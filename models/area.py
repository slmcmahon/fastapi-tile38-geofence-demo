from pydantic import BaseModel, field_validator, ValidationError, ValidationInfo
from typing import List, Literal, Optional, Union


class Area(BaseModel):
    id: str
    key: str
    type: Literal["Polygon", "Radius"]
    coordinates: Union[List[List[float]], List[float]]
    radius: Optional[int] = None

    @field_validator("coordinates")
    def validate_coordinates(cls, v, info: ValidationInfo):
        # Access 'type' from the instance values
        area_type = info.data.get("type")
        if area_type == "Polygon":
            if len(v) < 4:
                raise ValueError(
                    "Polygon coordinates must contain at least 4 points")
            if v[0] != v[-1]:
                raise ValueError(
                    "First and last coordinates of a polygon must be the same")
        return v

    @field_validator("radius", mode="before")
    def validate_radius(cls, v, info: ValidationInfo):
        # Access 'type' from the instance values
        area_type = info.data.get("type")

        if area_type == "Polygon" and v is not None:
            raise ValueError("Radius can only be set for a point")
        if area_type == "Radius" and v is None:
            raise ValueError("Radius must be set for a point")
        return v

    def to_geojson(self) -> str:
        if self.type == "Polygon":
            return {
                "type": "Feature",
                "properties": {"id": self.id},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [self.coordinates],
                },
            }
        return {
            "type": "Feature",
            "properties": {"id": self.id},
            "geometry": {
                "type": "Point",
                "coordinates": self.coordinates,
                "radius": self.radius,
            },
        }
