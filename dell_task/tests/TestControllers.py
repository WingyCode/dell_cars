from unittest import TestCase

from peewee import *

from common.Controllers import Controllers
from common.Models import Builder, Models


class TestContollers(TestCase):
    def setUp(self):
        Controllers.CarController.init_database(SqliteDatabase('test.db'))

        self.cars = []
        self.engines = []
        acceleration = Builder.build_acceleration(120, 10.5)
        perf = Builder.build_perf_figures(octaneRating=1, acceleration=acceleration)
        ff = Builder.build_fuel_figures(speed=120, mpg=12.5, usageDescription="this is the desc")
        Controllers.CarController.add_engine(Builder.build_engine(capacity=123, num_cylinders=4, max_rpm=5000,
                                                                  manufacturer_code="f"))
        Controllers.CarController.add_engine(Builder.build_engine(capacity=140, num_cylinders=4, max_rpm=5000,
                                                                  manufacturer_code="a"))
        self.engines = Controllers.CarController.get_engines()
        self.cars += [Models.Car(owner_name="John", serial_number=1001, model_year=1998, code="F",
                                 vehicle_code="a",
                                 engine=self.engines[0],
                                 manufacturer="Ford",
                                 fuelFigures=ff,
                                 performanceFigures=perf,
                                 model="Focus", activationCode="test123")]

        self.cars += [Models.Car(owner_name="Kate", serial_number=1002, model_year=2015, code="A",
                                 vehicle_code="f",
                                 engine=self.engines[1],
                                 manufacturer="Audi",
                                 model="A4", activationCode="test124",
                                 fuelFigures=Models.FuelFigure(speed=140, mpg=10.5,
                                                               usageDescription="this is the desc 2"),
                                 performanceFigures=Models.PerformanceFigures(octaneRating=2, acceleration=Models.Acceleration(140,
                                                                                                               9.5)))]
        Controllers.CarController.add_car(self.cars[0])
        Controllers.CarController.add_car(self.cars[1])
        # self.assertEqual(controllers.CarController.cars_count(), 2)
        # self.assertTrue(controllers.CarController.add_car(self.cars[0]))
        # self.assertTrue(controllers.CarController.add_car(self.cars[1]))

    def tearDown(self):
        Controllers.CarController.clean()

    def test_clean_all(self):
        Controllers.CarController.clean()
        self.assertEqual(Controllers.CarController.cars_count(), 0)

    def test_car_count(self):
        cnt = Controllers.CarController.cars_count()
        self.assertEqual(cnt, 2)

    def test_get_cars(self):
        cars = Controllers.CarController.get_cars()
        self.assertEqual(len(cars), 2)
        self.assertEqual(cars[0].owner_name, self.cars[0].owner_name)
        self.assertEqual(cars[1].owner_name, self.cars[1].owner_name)

    def test_clean_cars(self):
        num_cars = Controllers.CarController.cars_count()
        self.assertEqual(num_cars, 2)
        Controllers.CarController.clean()
        num_cars = Controllers.CarController.cars_count()
        self.assertEqual(num_cars, 0)

    def test_get_car_by_id(self):
        car = Controllers.CarController.get_car(1)
        self.assertEqual(self.cars[0].owner_name, car.owner_name)
        car = Controllers.CarController.get_car(2)
        self.assertEqual(self.cars[1].owner_name, car.owner_name)

    def test_delete_car_by_id(self):
        num_cars = Controllers.CarController.cars_count()
        self.assertEqual(num_cars, 2)
        res = Controllers.CarController.delete_car(1)
        self.assertTrue(res)
        cars = Controllers.CarController.get_cars()
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].owner_name, self.cars[1].owner_name)

    def test_update_car(self):
        car = Controllers.CarController.get_car(1)
        car.owner_name = "Bob"
        car_updated = Controllers.CarController.update_car(car)
        self.assertEqual(car_updated, car)
        # car_changed = controllers.CarController.get_car(1)
        # self.assertEqual(car_changed, car)

    def test_update_car_engine(self):
        car = Controllers.CarController.get_car(1)
        car.engine.num_cylinders = 6
        Controllers.CarController.update_car(car)
        car_changed = Controllers.CarController.get_car(1)
        self.assertEqual(car_changed.engine.num_cylinders, 6)
        self.assertEqual(car_changed, car)

    def test_engine_decode(self):
        capacity = 5
        num_cyl = 4
        max_rpm = 5000
        manuf_code = "f"
        engine = Controllers.CarController.engine_decode({"capacity": capacity, "num_cylinders": num_cyl,
                                                          "max_rpm": max_rpm, "manufacturer_code": manuf_code})
        self.assertEqual(engine.capacity, capacity)
        self.assertEqual(engine.num_cylinders, num_cyl)
        self.assertEqual(engine.max_rpm, max_rpm)
        self.assertEqual(engine.manufacturer_code, manuf_code)

    def test_fuelfigures_decode(self):
        speed = 150
        mpg = 15.5
        usage_description = "desc"
        ff = Controllers.CarController.fuel_figures_decode({"speed": speed, "mpg": mpg,
                                                          "usageDescription": usage_description})
        self.assertEqual(ff.speed, speed)
        self.assertEqual(ff.mpg, mpg)
        self.assertEqual(ff.usageDescription, usage_description)


    def test_performance_figures_decode(self):
        acceleration_mph = 16
        acceleration_seconds = 10.5
        octaneRating=10

        pf = Controllers.CarController.performance_figures_decode({"acceleration": {"mph": acceleration_mph,
                                                                                    "seconds":acceleration_seconds},
                                                                   "octaneRating": octaneRating})
        self.assertEqual(pf.octaneRating, octaneRating)
        self.assertEqual(pf.get_acceleration().mph, acceleration_mph)
        self.assertEqual(pf.get_acceleration().seconds, acceleration_seconds)

    def test_car_decode(self):
        owner_name = "John"
        serial_number = 1001
        model_year = 1998
        code = "F"
        vehicle_code = "a"
        capacity = 5
        num_cyl = 4
        max_rpm = 5000
        manuf_code = "f"
        manufacturer = "Ford"
        model = "Focus"
        activationCode = "test31223"
        speed = 150
        mpg = 15.5
        usage_description = "desc"
        acceleration_mph = 16
        acceleration_seconds = 10.5
        octaneRating = 10

        car = Controllers.CarController.car_decode({"ownerName": owner_name, "serialNumber": serial_number,
                                                    "modelYear": model_year, "code": code, "vehicleCode": vehicle_code,
                                                    "model": model, "activationCode": activationCode,
                                                    "engine": {"capacity": capacity, "num_cylinders": num_cyl,
                                                          "max_rpm": max_rpm, "manufacturer_code": manuf_code},
                                                    "fuelFigures": {"speed": speed, "mpg": mpg,
                                                          "usageDescription": usage_description},
                                                    "performanceFigures": {"acceleration": {"mph": acceleration_mph,
                                                                                    "seconds":acceleration_seconds},
                                                                   "octaneRating": octaneRating},
                                                    "manufacturer": manufacturer})
        self.assertEqual(car.owner_name, owner_name)
        self.assertEqual(car.engine.capacity, capacity)
        self.assertEqual(car.fuelFigures.speed, speed)
        self.assertEqual(car.performanceFigures.octaneRating, octaneRating)

    def test_update_car_fuel_figures(self):
        car = Controllers.CarController.get_car(1)
        car.fuelFigures.speed = 300
        Controllers.CarController.update_car(car)
        car_changed = Controllers.CarController.get_car(1)
        self.assertEqual(car_changed.fuelFigures.speed, 300)
        self.assertEqual(car_changed.fuelFigures.mpg, 12.5)

    def test_update_car_perf_figures(self):
        car = Controllers.CarController.get_car(1)
        car.performanceFigures.octaneRating = 12
        Controllers.CarController.update_car(car)
        car_changed = Controllers.CarController.get_car(1)
        self.assertEqual(car_changed.performanceFigures.octaneRating, 12)

    def test_add_existing_car(self):
        car = Models.Car.get(1)
        self.assertRaises(IntegrityError, Controllers.CarController.add_car, car)
        self.assertEqual(Controllers.CarController.cars_count(), 2)
        engines = Models.Engine.select()
        self.assertEqual(len(engines), 2)
        ffs = Models.FuelFigure.select()
        self.assertEqual(len(ffs), 2)
        pfs = Models.PerformanceFigures.select()
        self.assertEqual(len(pfs), 2)

    def test_add_with_same_engine(self):
        engine = Models.Engine.get(1)
        car = Models.Car(owner_name="Jill", serial_number=1003, model_year=2013, code="H",
                         vehicle_code="h",
                         engine=engine,
                         manufacturer="Hyundai", model="solaris", activationCode="test321",
                         fuelFigures=Models.FuelFigure(speed=110, mpg=11.5,
                                                       usageDescription="this is the desc 3"),
                         performanceFigures=Models.PerformanceFigures(octaneRating=3, acceleration=Models.Acceleration(100, 11.5)))
        self.assertEqual(Controllers.CarController.cars_count(), 2)
        self.assertEqual(len(Models.Engine.select()), 2)
        Controllers.CarController.add_car(car)
        self.assertEqual(Controllers.CarController.cars_count(), 3)
        self.assertEqual(len(Models.Engine.select()), 2)

    def test_car_not_exists(self):
        self.assertRaises(Exception, Controllers.CarController.get_car, 3)

    def test_engine_not_exists(self):
        self.assertRaises(Exception, Controllers.CarController.get_engine, 4)

    def test_engine_delete(self):
        eng = Controllers.CarController.get_engine(2)
        self.assertEqual(len(Controllers.CarController.get_engines()), 2)
        Controllers.CarController.delete_engine(1)
        self.assertEqual(len(Controllers.CarController.get_engines()), 1)
        self.assertEqual(Controllers.CarController.get_engines()[0], eng)

    def test_engine_delete_not_existing(self):
        eng1 = Controllers.CarController.get_engine(1)
        eng2 = Controllers.CarController.get_engine(2)
        self.assertEqual(len(Controllers.CarController.get_engines()), 2)
        self.assertRaises(Exception, Controllers.CarController.delete_engine, 3)
        self.assertEqual(len(Controllers.CarController.get_engines()), 2)
        self.assertEqual(Controllers.CarController.get_engines()[0], eng1)
        self.assertEqual(Controllers.CarController.get_engines()[1], eng2)

    def test_update_engine_by_id(self):
        eng = Controllers.CarController.get_engine(1)
        eng.num_cylinders = 6
        eng_changed = Controllers.CarController.update_engine(eng, 2)
        self.assertEqual(Controllers.CarController.get_engine(1).num_cylinders, 4)
        self.assertEqual(Controllers.CarController.get_engine(2).num_cylinders, 6)

    def test_update_engine_by_incorrect_id(self):
        eng = Controllers.CarController.get_engine(1)
        eng.num_cylinders = 6
        self.assertRaises(Exception, Controllers.CarController.update_engine, [eng, 4])

    # class MyThread(Thread):
    #     db = None
    #     car = None
    #
    #     def run(self):
    #         controllers.CarController.update_car(self.car)
    #
    # def test_parallel_update(self):
    #     # def upd_car():
    #     #     print("test")
    #     #     car_changed = models.Car.get(1)
    #     #     car_changed.serial_number += 1
    #     #     controllers.CarController.update_car(car_changed)
    #
    #     car = models.Car.get(1)
    #     init_serial_num = car.serial_number
    #     # for i in range(10):
    #     thread = self.MyThread()
    #     thread.db = models.db
    #     thread.car = car
    #     thread.start()
    #     car = models.Car.get(1)
    #     self.assertEqual(car.serial_number, init_serial_num)
