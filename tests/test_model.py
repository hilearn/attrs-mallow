from unittest import TestCase

from tests.models import StatesData, Zcta5


class ModelTest(TestCase):
    def test_states_data(self):
        obj = StatesData.schema().loads(
            '{"name": "California", "abbreviation": "CA"}')
        self.assertEqual(obj.name, "California")
        self.assertEqual(obj.abbreviation, "CA")

        obj = StatesData.schema().loads('{"abbreviation": "CA"}')
        self.assertIsNone(obj.name)
        self.assertEqual(obj.abbreviation, "CA")

    def test_derive(self):
        obj = Zcta5.schema().loads(
            '{"zcta": "0123", "geometry": {}, "state": "CA"}')
        self.assertEqual(obj.zcta, "0123")
        self.assertEqual(obj.state, "CA")
        self.assertDictEqual(obj.geometry, {})

        obj = Zcta5.schema().loads(
            '{"zcta": "0123", "state": "CA"}')
        self.assertIsNone(obj.geometry)
