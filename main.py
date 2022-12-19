import json
from typing import Union, List
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from models.test import Test
from models.server import Interval
from prometheus_client import start_http_server
from infra import logger
from business_logic import thread_task
from business_logic import globals
from infra import create_html_tabel
import collections

globals.init()
logger = logger.setup_custom_logger('root')

start_http_server(5000)
app = FastAPI()

with open('resources/data.json', 'r') as f:
    data = json.load(f)
    for req in data:
        globals.requests_list.append(req)
    print(globals.requests_list)

thread_task.start_req(globals.interval)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status", response_class=HTMLResponse)
def get_html_status():
    result_copy = globals.deq_result.copy()
    result_copy.reverse()
    return create_html_tabel.create_html_tbale(result_copy)


@app.get("/results", tags=["Results"])
def get_bit_results():
    return globals.deq_raw


@app.get("/process", tags=["Results"])
def get_bit_process_results():
    return globals.deq_result


@app.get("/requests", response_model=List[Test], tags=["Requests"])
def get_request_list():
    return globals.requests_list


@app.put("/requests", response_model=List[Test], tags=["Requests"])
def add_new_or_edit_request(request: Test):
    req = json.loads(request.json())
    globals.requests_list = list(filter(lambda x: x["id"] != req["id"], globals.requests_list))
    globals.requests_list.append(req)
    return globals.requests_list


@app.get("/request/{id}", response_model=List[Test], tags=["Requests"])
def get_request_by_id(item_id: int):
    result = list(filter(lambda x: x["id"] == item_id, globals.requests_list))
    return result

@app.get("/request/exe/{id}", response_model=List[Test], tags=["Requests"])
def execute_request_by_id(item_id: int):
    req = list(filter(lambda x: x["id"] == item_id, globals.requests_list))
    thread_task.test(req,"User")
    return req

@app.delete("/request/{id}", response_model=List[Test], tags=["Requests"])
def delete_request_by_id(item_id: int):
    globals.requests_list = list(filter(lambda x: x["id"] != item_id, globals.requests_list))
    return globals.requests_list


@app.get("/server/stop/{Are_you_sure}", tags=["Server"])
def stop_server(Are_you_sure: str):
    if Are_you_sure == "YES":
        globals.stop_threads = True
    return {"status": "Stopped"}


@app.get("/server/start/{Are_you_sure}", tags=["Server"])
def start_server(Are_you_sure: str):
    if Are_you_sure == "YES":
        if globals.stop_threads == True:
            globals.stop_threads = False
            thread_task.start_req(globals.interval)
    return {"status": "started"}


@app.get("/server/interval", tags=["Server"])
def get_server_interval():
    return {"interval": f"The requests executed once every {str(globals.interval / 60)} minutes "}


@app.post("/server/interval", tags=["Server"])
def update_server_interval_minutes(inter: Interval):
    if inter.interval > 0:
        globals.interval = inter.interval * 60
        return {"interval": f"The requests will be executed once every {str(globals.interval / 60)} minutes "}
    else:
        raise HTTPException(
            status_code=500, detail=f"Interval must be bigger then  0 "
        )
