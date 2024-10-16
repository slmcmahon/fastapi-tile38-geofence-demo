import unittest
from pydantic import ValidationError
from models.area import Area


class TestAreaModel(unittest.TestCase):

    def test_polygon_initialization(self):
        area = Area(
            id="123",
            key="key1",
            type="Polygon",
            coordinates=[[-74.04644050743283, 4.683776645270157],
                         [-74.04669426930562, 4.683220898829674],
                         [-74.04631362649623, 4.683041196292621],
                         [-74.04601979695919, 4.683583631586032],
                         [-74.04644050743283, 4.683776645270157]]
        )
        self.assertEqual(area.id, "123")
        self.assertEqual(area.type, "Polygon")
        self.assertEqual(len(area.coordinates), 5)

    def test_radius_initialization(self):
        area = Area(
            id="456",
            key="key2",
            type="Radius",
            coordinates=[-74.04644050743283, 4.683776645270157],
            radius=100
        )
        self.assertEqual(area.id, "456")
        self.assertEqual(area.type, "Radius")
        self.assertEqual(area.coordinates,
                         [-74.04644050743283, 4.683776645270157])
        self.assertEqual(area.radius, 100)

    def test_polygon_to_geojson(self):
        area = Area(
            id="123",
            key="key1",
            type="Polygon",
            coordinates=[[-74.04644050743283, 4.683776645270157],
                         [-74.04669426930562, 4.683220898829674],
                         [-74.04631362649623, 4.683041196292621],
                         [-74.04601979695919, 4.683583631586032],
                         [-74.04644050743283, 4.683776645270157]]
        )
        geojson = area.to_geojson()
        expected_geojson = {
            "type": "Feature",
            "properties": {"id": "123"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-74.04644050743283, 4.683776645270157],
                                 [-74.04669426930562, 4.683220898829674],
                                 [-74.04631362649623, 4.683041196292621],
                                 [-74.04601979695919, 4.683583631586032],
                                 [-74.04644050743283, 4.683776645270157]]],
            },
        }
        self.assertEqual(geojson, expected_geojson)

    def test_radius_to_geojson(self):
        area = Area(
            id="456",
            key="key2",
            type="Radius",
            coordinates=[-74.04644050743283, 4.683776645270157],
            radius=100
        )
        geojson = area.to_geojson()
        expected_geojson = {
            "type": "Feature",
            "properties": {"id": "456"},
            "geometry": {
                "type": "Point",
                "coordinates": [-74.04644050743283, 4.683776645270157],
                "radius": 100,
            },
        }
        self.assertEqual(geojson, expected_geojson)

    def test_invalid_coordinates(self):
        with self.assertRaises(ValidationError):
            # Trying to pass invalid coordinates for a Polygon
            Area(
                id="789",
                key="key3",
                type="Polygon",
                # Invalid, Polygon should have a list of lists
                coordinates=[-74.04644050743283, 4.683776645270157]
            )

    def test_missing_radius_for_radius_type(self):
        with self.assertRaises(ValidationError):
            # A "Radius" type must have a radius
            Area(
                id="789",
                key="key3",
                type="Radius",
                coordinates=[-74.04644050743283, 4.683776645270157]
            )


if __name__ == '__main__':
    unittest.main()
