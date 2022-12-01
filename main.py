import json
from typing import Union, List
from fastapi import FastAPI
from models.item import Item



app = FastAPI()

a = []
z = Item(name="jnk", price=7, is_offer=True)
z1 = Item(name="jnk", price=7, is_offer=True)
a.append(z)
a.append(z1)


with open('data.json', 'r') as f:
    data = json.load(f)

for kkk in data:
    ddd = Item(**kkk)
    a.append(ddd)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/jnk/",response_model=List[Item])
def read_root():
    return a


@app.post("/jnk/new")
def append_a(item: Item):
    a.append(item)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
