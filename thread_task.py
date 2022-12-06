from time import sleep
from threading import Thread
import settings
from  API.APIs import APIs
from collections import deque
import compare

# task that runs at a fixed interval
def background_task(interval_sec):
    # run forever
    my_req = settings.requests_list
    while True:
        # block for the interval
        sleep(interval_sec)
        # perform the task
        get_pet = APIs('https://petstore3.swagger.io/api/v3')
        for req in my_req:
            res = get_pet.get(req["request"]["path"])
            print(f"res = {res} with type {type(res)}")
            print(f'expected = {req["expected"]} with type {type(req["expected"])}')
            if isinstance(res, int):
                print("INTTTTTTTTTTTTT")
                pass
            else:
                print("I was here")
                if compare.compare(req["expected"],res):
                    print("YYYYYY")
            settings.deq.append(res)

        #global stop_threads
        if settings.stop_threads:
            break

def start_req():
    print('Starting background task...')
    daemon = Thread(target=background_task, args=(10,), daemon=True, name='Background')
    daemon.start()

# #stop_threads = False
# # create and start the daemon thread
#
# # main thread is carrying on...
# print('Main thread is carrying on...')
# val = input("Enter your value: ")
# stop_threads = True
# print('Main thread done.')