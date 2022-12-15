from pydantic import BaseModel
from typing import Union
from models.request import Request
from models.expected import Expected
# {"id": 1,"request":{"url": "https://petstore3.swagger.io/api/v3", "path": "pet/1", "type": "get"},"expected":{"name": "doggie","status": "sold"}},
class Test(BaseModel):
    id: int
    request: Request
    expected: Expected
