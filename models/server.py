from pydantic import BaseModel
from typing import Union


class Interval(BaseModel):
    interval: int
