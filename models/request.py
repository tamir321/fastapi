from pydantic import BaseModel
from typing import Union
from enum import Enum


# {"id": 1,"request":{"url": "https://petstore3.swagger.io/api/v3", "path": "pet/1", "type": "get"},"expected":{"name": "doggie","status": "sold"}},
class RequestType(str, Enum):
    get = 'get'
    post = 'post'
    put = 'put'
    delete = 'delete'


class Request(BaseModel):
    url: str
    path: str
    type: str
    #body: Union[dict, None] = None
