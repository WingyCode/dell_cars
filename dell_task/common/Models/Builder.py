from common.Models import Models


def build_engine(capacity, num_cylinders, max_rpm, manufacturer_code):
    return Models.Engine(capacity=capacity, num_cylinders=num_cylinders, max_rpm=max_rpm,
                         manufacturer_code=manufacturer_code)


def build_car(owner_name, serial_number, model_year, code, vehicle_code, engine, manufacturer, fuelFigures,
              performanceFigures, model, activationCode):
    return Models.Car(owner_name=owner_name, serial_number=serial_number,
                      model_year=model_year, code=code, vehicle_code=vehicle_code,
                      engine=engine, manufacturer=manufacturer, fuelFigures=fuelFigures,
                      performanceFigures=performanceFigures, model=model, activationCode=activationCode)


def build_fuel_figures(speed, mpg, usageDescription):
    return Models.FuelFigure(speed=speed, mpg=mpg, usageDescription=usageDescription)


def build_perf_figures(octaneRating, acceleration):
    return Models.PerformanceFigures(octaneRating=octaneRating, acceleration=acceleration)


def build_acceleration(mph, seconds):
    return Models.Acceleration(mph, seconds)