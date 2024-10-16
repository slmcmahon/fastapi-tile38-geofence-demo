from pydantic import BaseModel
from typing import List, Union


class Geometry(BaseModel):
    coordinates: List[Union[float, List[List[float]]]]
    type: str


class Properties(BaseModel):
    key: str
    id: str


class Feature(BaseModel):
    type: str
    properties: Properties
    geometry: Geometry
