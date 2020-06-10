import unittest

from models import Entity, Question


class TestModels(unittest.TestCase):
    def test_model_map(self):
        entity = Entity(
            name='Dássone', email='dyotamo@gmail.com', password='xyz')
        self.assertEqual(entity.to_map(), {
                         'name': 'Dássone', 'email': 'dyotamo@gmail.com'})


if __name__ == '__main__':
    unittest.main()
