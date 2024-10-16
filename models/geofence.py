from pydantic import BaseModel, field_validator
from typing import List
from enum import Enum


class GeofenceEvent(str, Enum):
    ENTER = "enter",
    EXIT = "exit",
    INSIDE = "inside",
    OUTSIDE = "outside",
    CROSSED = "crossed"


class Geofence(BaseModel):
    name: str
    url: str
    events: List[GeofenceEvent]
    object_key: str
    area_key: str
    radius: int = 1000

    class Config:
        use_enum_values = True

    @field_validator('events')
    def check_events(cls, v):
        if len(v) < 1:
            raise ValueError('events must contain at least one item')
        return v

    @field_validator('url')
    def check_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError('The URL must start with "http://" or "https://"')
        return v
