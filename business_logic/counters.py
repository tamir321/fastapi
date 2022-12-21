from prometheus_client import Counter , Summary

connection_fail_counter = Counter('fail_to_connect', 'fail to connect to server ')
request_counter = Counter('request_counter', 'Description of counter')
compare_fail_counter = Counter('compare_fail_counter', 'Description of counter')
REQUESTS_TIME = Summary('requests_processing_seconds', 'Time spent processing requests')