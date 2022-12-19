from collections import deque
import os


def init():
    global requests_list # move to
    global stop_threads
    global deq_raw
    global deq_result
    global interval
    global loop_id
    stop_threads = False
    requests_list = []
    stop_threads = False
    deq_raw = deque(maxlen=get_env('result_size',30))  # get from env
    deq_result = deque(maxlen=get_env('result_size',30))  # get from env
    interval = get_env('interval',600)
    loop_id = 100000


def get_env(env_key: str , default):
    return os.getenv(env_key) or default


def __str__(self):
    return "representation"