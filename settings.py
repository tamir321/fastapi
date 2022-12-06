from collections import deque



def init():
    global requests_list
    global stop_threads
    global deq
    requests_list = []
    stop_threads = False
    deq = deque(maxlen=10)
