from time import sleep
from threading import Thread
import settings
from  API.APIs import APIs
from prometheus_client import Counter

from collections import deque
import compare
import logging

logger = logging.getLogger('root')
connection_fail_counter = Counter('fail_to_connect', 'fail to connect to server ')
request_counter = Counter('request_counter', 'Description of counter')
compare_fail_counter = Counter('compare_fail_counter', 'Description of counter')


# task that runs at a fixed interval
def background_task(interval_sec):
    # run forever
    my_req = settings.requests_list
    while True:
        # block for the interval
        sleep(interval_sec)
        # perform the task
        #session = APIs('https://petstore3.swagger.io/api/v3')

        for req in my_req:
            #res = session.get(req["request"]["path"])
            res = request(req["request"])
            request_counter.inc()
            if isinstance(res, int):
                connection_fail_counter.inc()
                logger.error(f"result is not 200 {res} ")
                save_test_result(req,"Fail to connect to server",False)
            else:
                if compare.compare_arr(req["expected"],res):
                    logger.debug("result as expected")
                    save_test_result(req, "OK", True)
                else:
                    message = f'expected - {req["expected"]} to be equal to {res}'
                    logger.error(message)
                    save_test_result(req, message, False)
                    compare_fail_counter.inc()
            settings.deq_raw.append(res)

        #global stop_threads
        if settings.stop_threads:
            break

def start_req():
    print('Starting background task...')
    daemon = Thread(target=background_task, args=(10,), daemon=True, name='Background')
    daemon.start()

def save_test_result(req,result,test_pass):
    r= "Pass"
    if not test_pass:
        r = "fail"
    settings.deq_result.append({"req":req["request"],"result":result,"pass/fail":r})

#{"request":{"url": "https://petstore3.swagger.io/api/v3", "path": "pet/1", "type": "get"}
def request(req):
    session = APIs(req["url"])
    if req["type"] == "get":
        return session.get(req["path"])
    if req["type"] == "post":
        return session.post(req["path"],req["data"])


# #stop_threads = False
# # create and start the daemon thread
#
# # main thread is carrying on...
# print('Main thread is carrying on...')
# val = input("Enter your value: ")
# stop_threads = True
# print('Main thread done.')