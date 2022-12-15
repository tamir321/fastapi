from collections import deque


def init():
    global requests_list # move to
    global stop_threads
    global deq_raw
    global deq_result
    global interval
    stop_threads = False
    requests_list = []
    stop_threads = False
    deq_raw = deque(maxlen=10)  # get from env
    deq_result = deque(maxlen=10)  # get from env
    interval = 60

def __str__(self):
    return "representation"