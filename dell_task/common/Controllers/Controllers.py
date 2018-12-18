import atexit

from common.Models import Models, Builder


class CarController:
    @staticmethod
    def init_database(db):
        Models.db.initialize(db)
        Models.db.create_tables([Models.Engine, Models.PerformanceFigures, Models.FuelFigure, Models.Car,
                                 Models.Car])
        atexit.register(CarController.cleanup)

    @staticmethod
    def cleanup():
        # print("Cleanup: db is closed")
        Models.db.close()

    @staticmethod
    def add_car(car: Models.Car):
        with Models.db.atomic("Deferred") as txn:
            ff = Models.FuelFigure.create(speed=car.fuelFigures.speed, mpg=car.fuelFigures.mpg,
                                          usageDescription=car.fuelFigures.usageDescription)
            pf = Models.PerformanceFigures.create(octaneRating=car.performanceFigures.octaneRating,
                                                  acceleration=car.performanceFigures.acceleration)
            if car.engine.id is None:
                eng = Models.Engine.create(id=car.engine.id, capacity=car.engine.capacity,
                                           num_cylinders=car.engine.num_cylinders,
                                           max_rpm=car.engine.max_rpm, manufacturer_code=car.engine.manufacturer_code)
            else:
                eng = car.engine
            car = Models.Car.create(id=car.id, owner_name=car.owner_name, serial_number=car.serial_number,
                                    model_year=car.model_year, code=car.code, vehicle_code=car.vehicle_code,
                                    engine=eng, manufacturer=car.manufacturer, fuelFigures=ff,
                                    performanceFigures=pf, model=car.model, activationCode=car.activationCode)
            txn.commit()
            return car

    @staticmethod
    def get_cars():
        return Models.Car.select()

    @staticmethod
    def clean():
        with Models.db.atomic() as txn:
            Models.Car.delete().execute()
            Models.Engine.delete().execute()
            Models.FuelFigure.delete().execute()
            Models.PerformanceFigures.delete().execute()
            txn.commit()

    @staticmethod
    def get_car(id):
        return Models.Car.get(Models.Car.id == id)

    @staticmethod
    def delete_car(id):
        try:
            with Models.db.atomic() as txn:
                to_del = Models.Car.select().where(Models.Car.id == id)
                if to_del.count() == 0:
                    raise AttributeError("Car '{}' doesn't exists".format(id))
                Models.Car.delete().where(Models.Car.id == id).execute()
                txn.commit()
                return True
        except Exception as ex:
            raise

    @staticmethod
    def cars_count():
        return Models.Car.select().count()

    @staticmethod
    def update_engine(engine, id=None):
        if id is None:
            id = engine.id
        try:
            CarController.get_engine(id)
        except:
            raise AttributeError("Engine '{}' doesn't exists".format(id))
        with Models.db.atomic() as txn:

            Models.Engine.update({Models.Engine.capacity: engine.capacity,
                                  Models.Engine.num_cylinders: engine.num_cylinders,
                                  Models.Engine.max_rpm: engine.max_rpm,
                                  Models.Engine.manufacturer_code: engine.manufacturer_code}). \
                where(Models.Engine.id == id).execute()
            txn.commit()
            return CarController.get_engine(id)

    @staticmethod
    def update_performance_figures(performance_figures):
        with Models.db.atomic() as txn:
            Models.PerformanceFigures.update({Models.PerformanceFigures.octaneRating: performance_figures.octaneRating,
                                              Models.PerformanceFigures.acceleration: performance_figures.acceleration}).where(
                Models.PerformanceFigures.id == performance_figures.id).execute()
            txn.commit()

    @staticmethod
    def update_fuel_figures(ff_id, fuel_figures):
        with Models.db.atomic() as txn:
            Models.FuelFigure.update({Models.FuelFigure.speed: fuel_figures.speed,
                                      Models.FuelFigure.mpg: fuel_figures.mpg,
                                      Models.FuelFigure.usageDescription: fuel_figures.usageDescription}).where(
                Models.FuelFigure.id == ff_id).execute()
            txn.commit()

    @staticmethod
    def update_car(car, id=None):
        if id is None:
            id = car.id
        with Models.db.atomic() as txn:
            CarController.update_engine(car.engine, None if car.engine.id is not None else car.engine.id)
            CarController.update_fuel_figures(car.fuelFigures.id, car.fuelFigures)
            CarController.update_performance_figures(car.performanceFigures)
            Models.Car.update({Models.Car.owner_name: car.owner_name,
                               Models.Car.serial_number: car.serial_number,
                               Models.Car.model_year: car.model_year,
                               Models.Car.code: car.code,
                               Models.Car.vehicle_code: car.vehicle_code,
                               Models.Car.manufacturer: car.manufacturer,
                               Models.Car.performanceFigures: car.performanceFigures,
                               Models.Car.model: car.model,
                               Models.Car.activationCode: car.activationCode}).where(
                Models.Car.id == car.id).execute()
            txn.commit()
            return Models.Car.get(Models.Car.id == car.id)

    @staticmethod
    def get_engines():
        return Models.Engine.select()

    @staticmethod
    def get_engine(id):
        try:
            return Models.Engine.get(Models.Engine.id == id)
        except:
            raise AttributeError("Engine #{} not found".format(id))

    @staticmethod
    def add_engine(engine):
        with Models.db.atomic() as txn:
            engine = Models.Engine.create(capacity=engine.capacity, num_cylinders=engine.num_cylinders,
                                          max_rpm=engine.max_rpm,
                                          manufacturer_code=engine.manufacturer_code)
            txn.commit()
            return engine

    @staticmethod
    def delete_engine(id):
        try:
            with Models.db.atomic() as txn:
                to_del = Models.Engine.select().where(Models.Engine.id == id)
                if to_del.count() == 0:
                    raise AttributeError("Engine '{}' doesn't exists".format(id))
                Models.Engine.delete().where(Models.Engine.id == id).execute()
                txn.commit()
        except Exception as ex:
            raise

    @staticmethod
    def add_fuel_figures(ff):
        with Models.db.atomic() as txn:
            fuelFigures = Models.FuelFigure.create(speed=ff.speed, mpg=ff.mpg, usageDescription=ff.usageDescription)
            txn.commit()
            return fuelFigures

    @staticmethod
    def get_fuel_figures(id):
        try:
            return Models.FuelFigure.get(Models.FuelFigure.id == id)
        except:
            raise AttributeError("FuelFigure #{} not found".format(id))

    @staticmethod
    def add_performance_figures(pf):
        with Models.db.atomic() as txn:
            perf_figures = Models.PerformanceFigures.create(octaneRating=pf.octaneRating, acceleration=pf.acceleration)
            txn.commit()
            return perf_figures

    @staticmethod
    def get_performance_figures(id):
        try:
            return Models.PerformanceFigures.get(Models.PerformanceFigures.id == id)
        except:
            raise AttributeError("PerformanceFigures #{} not found".format(id))

    @staticmethod
    def performance_figures_decode(pf_json):
        if isinstance(pf_json, dict):
            acceleration = Builder.build_acceleration(pf_json["acceleration"]["mph"],
                                                      pf_json["acceleration"]["seconds"])
            pf = CarController.add_performance_figures(
                Builder.build_perf_figures(octaneRating=pf_json["octaneRating"],
                                           acceleration=acceleration))
        elif isinstance(pf_json, int):
            pf = CarController.get_performance_figures(pf_json)
        else:
            raise AttributeError("Incorrect PerformanceFigures property")
        return pf

    @staticmethod
    def fuel_figures_decode(ff_json):
        if isinstance(ff_json, dict):
            ff = Builder.build_fuel_figures(speed=ff_json["speed"],
                                            mpg=ff_json["mpg"],
                                            usageDescription=ff_json["usageDescription"])
        elif isinstance(ff_json, int):
            ff = CarController.get_fuel_figures(ff_json)
        else:
            raise AttributeError("Incorrect FuelFigures property")
        return ff

    @staticmethod
    def engine_decode(engine_json):
        if isinstance(engine_json, dict):
            engine = Builder.build_engine(capacity=engine_json["capacity"],
                                          num_cylinders=engine_json["num_cylinders"],
                                          max_rpm=engine_json["max_rpm"],
                                          manufacturer_code=engine_json["manufacturer_code"])
        elif isinstance(engine_json, int):
            engine = CarController.get_engine(engine_json)
        else:
            raise AttributeError("Incorrect Engine property")
        return engine

    @staticmethod
    def car_decode(car_json):
        engine = CarController.engine_decode(car_json["engine"])
        ff = CarController.fuel_figures_decode(car_json["fuelFigures"])
        pf = CarController.performance_figures_decode(car_json["performanceFigures"])
        car = CarController.add_car(Builder.build_car(owner_name=car_json["ownerName"],
                                                      serial_number=car_json["serialNumber"],
                                                      model_year=car_json["modelYear"],
                                                      code=car_json["code"],
                                                      vehicle_code=car_json["vehicleCode"],
                                                      engine=engine,
                                                      manufacturer=car_json["manufacturer"],
                                                      fuelFigures=ff,
                                                      performanceFigures=pf, model=car_json["model"],
                                                      activationCode=car_json["activationCode"]))
        return car
