import json
#from typing import Union, List
from fastapi import FastAPI
#from models.item import Item
from prometheus_client import start_http_server
# import settings
from infra import logger
from business_logic import thread_task
from business_logic import globals

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


with open('data.json', 'r') as f:
    data = json.load(f)
    for req in data:
        globals.requests_list.append(req)

#print(f"data= {data}")

thread_task.start_req()
# for kkk in data:
#     ddd = Item(**kkk)
#     a.append(ddd)
#



#print(f"requests_list= {settings.requests_list}")
@app.get("/")
def read_root():
    return {"Hello": "World"}


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

@app.get("/results")
def get_bit_results():
    return globals.deq_raw

@app.get("/process")
def get_bit_process_results():
    return globals.deq_result

@app.get("/requests")
def get_request_list():
    return globals.requests_list

@app.get("/request/{id}")
def get_request_by_id(item_id: int):
    list(filter(lambda x: x["id"] == item_id, globals.deq_result))
