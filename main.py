from fastapi import FastAPI

from typing import Union
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

items: Item = []

@app.get("/")
def root():
    item_dict = {}
    for item in items:
        item_dict[item.id] = item
    return item_dict

@app.get("/items/{item_id}")
def find_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return {"Item": item}
    return None

@app.put("/items/{item_id}")
def add_item(item_id: int, price: float, item: Item, name: Union[str, None] = None):
    item.id = item_id
    item.name = name
    item.price = price
    items.append(item)
    return {"Item": item}

@app.post("/items/{item_id}")
def update_item(item_id: int, new_price: float, new_name: Union[str, None] = None):
    item_exists = find_item(item_id)
    if item_exists != None:
        item_exists["Item"].id = item_id
        item_exists["Item"].name = new_name
        item_exists["Item"].price = new_price
        return {"Item": item_exists["Item"]}
        
@app.delete("/items/{item_id}")
def remove_item(item_id: int):
    item_exists = find_item(item_id)
    if item_exists != None:
        items.remove(item_exists["Item"])
        return {"Item": item_exists["Item"]}