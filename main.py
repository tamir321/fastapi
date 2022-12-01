# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from typing import Union
from fastapi import FastAPI
from models.item import Item


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# 325408706
app = FastAPI()

a = []
z = Item(name="jnk", price=7, is_offer=True)
z1 = Item(name="jnk", price=7, is_offer=True)
a.append(z)
a.append(z1)

print(a)
print(z.name)
print(z.json())

with open('data.json', 'r') as f:
    data = json.load(f)
# print(data)
# print(type(data))
print(len(data))

for kkk in data:
    print(kkk)
    ddd = Item(**kkk)
    a.append(ddd)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/jnk/")
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
