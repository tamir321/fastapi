import json
from typing import Union, List
from fastapi import FastAPI ,HTTPException
from fastapi.responses import HTMLResponse
from models.test import Test
from models.server import Interval
from prometheus_client import start_http_server
# import settings
from infra import logger
from business_logic import thread_task
from business_logic import globals
from infra import  create_html_tabel

#settings.init()
globals.init()
logger = logger.setup_custom_logger('root')

start_http_server(5000)
app = FastAPI()

# a = []
# z = Item(name="jnk", price=7, is_offer=True)
# z1 = Item(name="jnk", price=7, is_offer=True)
# a.append(z)
# a.append(z1)


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
    return create_html_tabel.create_html_tbale(globals.deq_result)

@app.get("/results",tags=["Results"])
def get_bit_results():
    return globals.deq_raw

@app.get("/process",tags=["Results"])
def get_bit_process_results():
    return globals.deq_result

@app.get("/requests",response_model=List[Test],tags=["Requests"])
def get_request_list():
    return globals.requests_list

@app.get("/request/{id}",response_model=List[Test],tags=["Requests"])
def get_request_by_id(item_id: int):
    result = list(filter(lambda x: x["id"] == item_id, globals.requests_list))
    return result

@app.get("/server/stop/{Are_you_sure}",tags=["Server"])
def stop_server(Are_you_sure: str):
    if Are_you_sure == "YES":
        globals.stop_threads = True
    return {"status": "Stopped"}


@app.get("/server/start/{Are_you_sure}",tags=["Server"])
def start_server(Are_you_sure: str):
    if Are_you_sure == "YES":
        if globals.stop_threads == True:
            globals.stop_threads = False
            thread_task.start_req(globals.interval)
    return {"status": "started"}

@app.get("/server/interval",tags=["Server"])
def get_server_interval():
    return {"interval": f"The requests executed once every {str(globals.interval/60)} minutes "}

@app.post("/server/interval",tags=["Server"])
def update_server_interval_minutes(inter: Interval):
    print(inter)
    print(type(inter.interval))
    if inter.interval >0:
        globals.interval = inter.interval * 60
        return {"interval": f"The requests will be executed once every {str(globals.interval / 60)} minutes "}
    else:
        raise HTTPException(
            status_code=500, detail=f"Interval must be bigger then  0 "
        )

#TODO: add request update/delete
#TODO: add read from env

# @app.get("/jnk/",response_model=List[Item])
# def read_root():
#     return a
#
#
# @app.post("/jnk/new")
# def append_a(item: Item):
#     a.append(item)
#
# @app.post("/jnk/new11")
# def append_a(item: Item):
#     a.append(item)
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


