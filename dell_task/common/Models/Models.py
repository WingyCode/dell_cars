import collections
import json

from peewee import *
from playhouse.sqlite_ext import JSONField

db = Proxy()  # SqliteDatabase('cars.db')


class BaseModel(Model):
    def __str__(self):
        r = {}
        for k in self.__data__.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

    class Meta:
        database = db


class Engine(BaseModel):
    capacity = IntegerField()  # uint16()
    num_cylinders = IntegerField()  # uint8()
    max_rpm = IntegerField()  # uint16()
    manufacturer_code = CharField()

    def __eq__(self, other):
        if not isinstance(other, Engine):
            raise AttributeError("Attribute should be of Engine type")

        if self.capacity != other.capacity:
            return False
        if self.num_cylinders != other.num_cylinders:
            return False
        if self.max_rpm != other.max_rpm:
            return False
        if self.manufacturer_code != other.manufacturer_code:
            return False

        return True

    def __ne__(self, other):
        return not self == other


class FuelFigure(BaseModel):
    speed = IntegerField()
    mpg = FloatField()
    usageDescription = TextField()

    def __eq__(self, other):
        if not isinstance(other, FuelFigure):
            raise AttributeError("Attribute should be of FuelFigure type")

        if self.speed != other.speed:
            return False
        if self.mpg != other.mpg:
            return False
        if self.usageDescription != other.usageDescription:
            return False

        return True

    def __ne__(self, other):
        return not self == other

# FuelFigure = collections.namedtuple("fuelFigures", "speed mpg usageDescription")
Acceleration = collections.namedtuple("acceleration", "mph seconds")


class PerformanceFigures(BaseModel):
    octaneRating = IntegerField()
    acceleration = JSONField(default=Acceleration(120, 10.5))

    def get_acceleration(self):
        return Acceleration(*self.acceleration)

    def __eq__(self, other):
        if not isinstance(other, PerformanceFigures):
            raise AttributeError("Attribute should be of PerformanceFigures type")

        if self.octaneRating != other.octaneRating:
            return False
        if self.get_acceleration() != other.get_acceleration():
            return False

        return True

    def __ne__(self, other):
        return not self == other


class Car(BaseModel):
    owner_name = CharField()
    serial_number = IntegerField()
    model_year = IntegerField()
    code = CharField()
    vehicle_code = CharField()
    engine = ForeignKeyField(Engine, related_name="engine")
    fuelFigures = ForeignKeyField(FuelFigure, related_name="fuelFigures")
    performanceFigures = ForeignKeyField(PerformanceFigures, related_name="performanceFigures")
    manufacturer = CharField()
    model = TextField()
    activationCode = TextField()

    def __eq__(self, other):
        if not isinstance(other, Car):
            raise AttributeError("Attribute should be of Car type")
        if self.owner_name != other.owner_name:
            return False
        if self.serial_number != other.serial_number:
            return False
        if self.model_year != other.model_year:
            return False
        if self.code != other.code:
            return False
        if self.vehicle_code != other.vehicle_code:
            return False
        if self.engine != other.engine:
            return False
        if self.fuelFigures != other.fuelFigures:
            return False
        if self.performanceFigures != other.performanceFigures:
            return False
        if self.manufacturer != other.manufacturer:
            return False
        if self.model != other.model:
            return False
        if self.activationCode != other.activationCode:
            return False

        return True

    def __ne__(self, other):
        return not self == other
