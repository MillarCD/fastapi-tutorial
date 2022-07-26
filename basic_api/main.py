from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class ModelName( str, Enum ):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

class Item(BaseModel):
    name: str
    description: str | None = None # optional
    price: float
    tax: float | None = None

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'hello world'}

@app.get('/items/me')
async def read_item():
    return {'item_id': 'the current user'}
"""
@app.get('/items/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}
"""

@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'deep learning FTW!'}
    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}
    
    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


# QUERY PARAMETERS
fake_items_db = [{'item_name': 'foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]

# function with query paramethers
# /items/?skip=0&limit=10
@app.get('/items/')
async def read_item(skip: int=0, limit: int=10):
    return fake_items_db[skip: skip+limit]

@app.get('/items/{item_id}')
async def read_item(item_id: str,needed: str, q: str | None = None):
    if q:  # las queries requires deben ir primero <---
        return {'item_id': item_id, 'q': q, 'needed': needed}
    return {'item_id': item_id, 'needed': needed}
"""
@app.get('/items/{item_id}')
async def read_item(item_id: str, needed: str):
    return {'item_id': item_id, 'needed': needed}
"""

# diferents orden of paramethers
@app.get('/users/{user_id}/items/{item_id}')
async def read_item(item_id: str, user_id: int,  q: str | None = None, short: bool=False):
    item = {'user_id': user_id, 'item_id': item_id}
    if q:
        item.update({'q': q})
    if short:
        item.update({'description': 'this is a description'})
    return item


# REQUEST BODY
@app.post('/items/')
async def create_item(item: Item):
    return item

# all in one
@app.post('/items/{item_id}')
async def create_item(item: Item, item_id: str, q: str | None = None):
    if q:
        return {'item_id': item_id, 'item': item, 'q': q}
    return {'item_id': item_id, 'item': item}
