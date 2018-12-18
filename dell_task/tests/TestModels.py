from unittest import TestCase
from peewee import *

from common.Models import Models

test_db = SqliteDatabase(':memory:')


class TestModels(TestCase):
    def setUp(self):
        Models.db.initialize(test_db)
        Models.Engine.create_table()
        Models.Car.create_table()
        Models.FuelFigure.create_table()
        Models.PerformanceFigures.create_table()

        self.engine = Models.Engine.create(capacity=123, num_cylinders=4, max_rpm=5000, manufacturer_code="f")
        self.fuel_figure = Models.FuelFigure.create(speed=120, mpg=12.5, usageDescription="this is the desc")
        self.perf_figures = Models.PerformanceFigures.create(octaneRating=1, acceleration=Models.Acceleration(120, 10.5))
        self.car = Models.Car.create(owner_name="John", serial_number=1001, model_year=1998, code="F",
                                     vehicle_code="a", engine=self.engine, manufacturer="Ford",
                                     fuelFigures=self.fuel_figure, performanceFigures=self.perf_figures, model="Focus",
                                     activationCode="test123")

    def tearDown(self):
        try:
            Models.Engine.drop_table()
            Models.FuelFigure.drop_table()
            Models.PerformanceFigures.drop_table()
            Models.Car.drop_table()
        except:
            pass
        Models.db.close()

    def test_get_engine(self):
        e = Models.Engine.get(1)
        self.assertEqual(e, self.engine)

    def test_delete_engine(self):
        cnt = Models.Engine.select().count()
        self.assertEqual(cnt, 1)
        Models.Engine.get(1).delete_instance()
        cnt = Models.Engine.select().count()
        self.assertEqual(cnt, 0)

    def test_get_car(self):
        c = Models.Car.get(1)
        self.assertEqual(c, self.car)
        self.assertEqual(c.engine, self.engine)
        self.assertEqual(c.fuelFigures, self.fuel_figure)
        self.assertEqual(c.performanceFigures, self.perf_figures)

    def test_car_eq(self):
        car = Models.Car.get(1)
        self.assertEqual(self.car, car)

    def test_car_ne(self):
        car = Models.Car.get(1)
        car.owner_name = "other"
        self.assertNotEqual(self.car, car)

    def test_engine_eq(self):
        car = Models.Car.get(1)
        self.assertEqual(self.car.engine, car.engine)

    def test_engine_ne(self):
        car = Models.Car.get(1)
        car.engine.num_cylinders = 6
        self.assertNotEqual(self.car.engine, car.engine)

    def test_fuel_figures_eq(self):
        car = Models.Car.get(1)
        self.assertEqual(self.car.fuelFigures, car.fuelFigures)

    def test_fuel_figures_ne(self):
        car = Models.Car.get(1)
        car.fuelFigures.speed = 200
        self.assertNotEqual(self.car.fuelFigures, car.fuelFigures)
