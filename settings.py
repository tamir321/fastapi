from collections import deque



def init():
    global requests_list
    global stop_threads
    global deq_raw
    global deq_result
    requests_list = []
    stop_threads = False
    deq_raw = deque(maxlen=10)
    deq_result = deque(maxlen=10)
