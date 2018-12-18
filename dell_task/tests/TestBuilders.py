from unittest import TestCase
from common.Models import Builder


class TestBuilders(TestCase):
    def test_build_engine(self):
        engine = Builder.build_engine(capacity=1, num_cylinders=2, max_rpm=3, manufacturer_code=4)
        self.assertEqual(engine.capacity, 1)
        self.assertEqual(engine.num_cylinders, 2)
        self.assertEqual(engine.max_rpm, 3)
        self.assertEqual(engine.manufacturer_code, 4)
