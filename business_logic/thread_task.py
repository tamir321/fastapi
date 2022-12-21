from time import sleep, time, ctime
from threading import Thread
from business_logic import globals
from API.APIs import APIs
# from prometheus_client import Counter
from business_logic import compare
from infra import logger
from datetime import datetime
from business_logic.counters import *

logger = logger.setup_custom_logger('root')


# task that runs at a fixed interval
def background_task(interval_sec):
    # run forever
    my_req = globals.requests_list  # bug
    while True:
        test(my_req)
        sleep(interval_sec)
        if globals.stop_threads:
            save_test_result({"Warning": "Warning"}, "The server was stopped", False)
            break


def start_req(interval_sec):
    print('Starting background task...')
    daemon = Thread(target=background_task, args=(interval_sec,), daemon=True, name='Background')
    daemon.start()


def singl_test(test_id: int):
    req = list(filter(lambda x: x["id"] == test_id, globals.requests_list))
    test(req)


@REQUESTS_TIME.time()
def test(my_req, initiator="Auto"):
    globals.loop_id += 1
    start = time()
    tests = 0
    pass_test = 0
    for req in my_req:  # settings.requests_list
        tests += 1
        res = request(req["request"], req["expected"]["status"])
        request_counter.inc()
        if isinstance(res, int):
            connection_fail_counter.inc()
            logger.error(f"result is not 200 {res} ")
            save_test_result(req,
                             f"Fail to connect to server received status {res} expected {req['expected']['status']}",
                             False, initiator)
        else:
            if compare.compare_arr(req["expected"], res):
                logger.debug("result as expected")
                pass_test += 1
                save_test_result(req, "OK", True, initiator)
            else:
                message = f'expected - {req["expected"]["data"]} to be equal to {res}'
                logger.error(message)
                save_test_result(req, message, False, initiator)
                compare_fail_counter.inc()
        globals.deq_raw.append(res)
    end = time()
    save_test_result({"request": f"started at {ctime(start)} ended at {ctime(end)} duration [sec] {end - start}"},
                     f"Total requests={tests}  Pass-{pass_test} Failed-{tests - pass_test}", tests == pass_test,
                     initiator)
    return start - end


def save_test_result(req, result, test_pass, initiator="Auto"):
    r = "Pass"
    message = ""
    if not test_pass:
        r = "Fail"
    if "request" in req.keys():
        message = req["request"]
    summery = {"Time": {"Time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Interaction": globals.loop_id},
               "req": message, "result": result, "pass/fail": r,
               "Initiator": initiator}
    globals.deq_result.append(summery)
    logger.info(summery)


def request(req, expected_status=200):
    session = APIs(req["url"])
    if req["type"] == "get":
        res = session.get(path=req["path"], expected_status=expected_status)
    if req["type"] == "post":
        res = session.post(path=req["path"], body=["data"], expected_status=expected_status)
    session.close()
    return res
