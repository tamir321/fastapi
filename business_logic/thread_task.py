from time import sleep
from threading import Thread
from business_logic import globals
from API.APIs import APIs
from prometheus_client import Counter
from business_logic import compare
from infra import logger
from datetime import datetime

logger = logger.setup_custom_logger('root')
connection_fail_counter = Counter('fail_to_connect', 'fail to connect to server ')
request_counter = Counter('request_counter', 'Description of counter')
compare_fail_counter = Counter('compare_fail_counter', 'Description of counter')



# task that runs at a fixed interval
def background_task(interval_sec):
    # run forever
    my_req = globals.requests_list  # bug
    while True:
        # block for the interval
        sleep(interval_sec)

        for req in my_req:  # settings.requests_list
            # res = session.get(req["request"]["path"])
            res = request(req["request"],req["expected"]["status"])
            request_counter.inc()
            if isinstance(res, int):
                connection_fail_counter.inc()
                logger.error(f"result is not 200 {res} ")
                save_test_result(req, f"Fail to connect to server received status {res} expected {req['expected']['status']}", False)
            else:
                if compare.compare_arr(req["expected"], res):
                    logger.debug("result as expected")
                    save_test_result(req, "OK", True)
                else:
                    message = f'expected - {req["expected"]["data"]} to be equal to {res}'
                    logger.error(message)
                    save_test_result(req, message, False)
                    compare_fail_counter.inc()
            globals.deq_raw.append(res)

        # global stop_threads
        if globals.stop_threads:
            save_test_result({"Warning":"Warning"},"The server was stopped",False)
            print("@@@@@@@@@@@@stoped@@@@@@@@@@@@@@")
            break


def start_req(interval_sec):
    print('Starting background task...')
    daemon = Thread(target=background_task, args=(interval_sec,), daemon=True, name='Background')
    daemon.start()


def save_test_result(req, result, test_pass):
    r = "Pass"
    message = ""
    if not test_pass:
        r = "Fail"
    if "request" in req.keys():
        message = req["request"]
    globals.deq_result.append({"Time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),"req": message , "result": result, "pass/fail": r})


# {"request":{"url": "https://petstore3.swagger.io/api/v3", "path": "pet/1", "type": "get"}
def request(req, expected_status=200):
    session = APIs(req["url"])
    if req["type"] == "get":
        return session.get(path=req["path"], expected_status=expected_status)
    if req["type"] == "post":
        return session.post(path=req["path"], body=["data"], expected_status=expected_status)

# post(self, path, body, expected_status=200):
# #stop_threads = False
# # create and start the daemon thread
#
# # main thread is carrying on...
# print('Main thread is carrying on...')
# val = input("Enter your value: ")
# stop_threads = True
# print('Main thread done.')
