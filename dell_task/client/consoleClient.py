import requests
import json

from common.Models import Builder


def main():
    print("Welcome!")
    print("")

    while True:
        print("What would you like to do?")
        print(" 1 Get the list of cars")
        print(" 2 Get the car by id")
        print(" 3 Add new car")
        print(" 4 delete the car by id")
        print(" Q to exit")
        answ = input()
        if answ.lower() == "q":
            break
        try:
            execute_action(answ)
        except Exception as ex:
            print("ERROR: {}. Try again".format(ex))
            print("")

    print("Thanks, bye!")
    # r = requests.get("http://localhost:5000/cars")
    # print(r.status_code)


def execute_action(answ):
    try:
        answ = int(answ)
    except:
        raise AttributeError("incorrect input!")

    try:
        if answ == 1:
            res = get_all_cars()
        elif answ ==2:
            id = get_id()
            res = get_car_by_id(id)
        elif answ == 3:
            res = add_new_car()
        elif answ == 4:
            id = get_id()
            res = delete_car_by_id(id)

        if res:
            print("Success!")
            print("")
        else:
            print("Action failed")
            print("")
    except Exception as ex:
        print("Action failed ({})".format(ex))


def get_id():
    try:
        id = int(input("Enter car id: "))
    except:
        raise Exception("Incorrect id, should be int")
    return id


def ask_y_n(msg):
    ans = "b"
    while ans.lower() != "y" and ans.lower() != "n":
        ans = input("{} (Y/n)".format(msg))
        if ans == "":
            ans = "y"
        # if ans == "y" or ans == "n":
        #     break
    return True if ans.lower() == "y" else False


def engine_exists(id=None):
    r = requests.get("http://localhost:5000/engines/{}".format(id))
    if r.status_code == 200:
        return True
    else:
        return False


def get_perf_figures(id):
    r = requests.get("http://localhost:5000/performanceFigures/{}".format(id))
    if r.status_code == 200:
        return json.loads(r.json()["performanceFigures"])
    else:
        return None


def get_fuel_figues(id):
    r = requests.get("http://localhost:5000/fuelFigures/{}".format(id))
    if r.status_code == 200:
        return json.loads(r.json()["fuelFigures"])
    else:
        return None


def get_engine(id):
    r = requests.get("http://localhost:5000/engines/{}".format(id))
    if r.status_code == 200:
        return json.loads(r.json()["engine"])
    else:
        return None


def add_new_car():
    try:
        ownerName = input("ownerName: ")
        serialNumber = input("serialNumber: ")
        modelYear = input("modelYear: ")
        code = input("code: ")
        vehicleCode = input("vehicleCode: ")
        while True:
            if ask_y_n("Would you like to create new engine? (use existing number if no)"):
                engine = Builder.build_engine(capacity=input("   capacity: "),
                                              num_cylinders=input("   num_cylinders: "),
                                              max_rpm=input("   max_rpm: "),
                                              manufacturer_code=input("   manufacturer_code: "))
                break
            else:
                try:
                    engine = int(input("Engine id:"))
                    if not engine_exists(engine):
                        raise Exception
                    break
                except:
                    print("Incorrect engine id! Try again...")
                    continue
        speed = input("speed: ")
        mpg = input("mpg: ")
        usageDescription = input("usageDescriptio1n: ")

        octaneRating = input("octaneRating: ")
        acceleration_mph = input("acceleration, mph: ")
        acceleration_seconds = input("acceleration, seconds: ")
        manufacturer = input("manufacturer: ")
        model = input("model: ")
        activationCode = input("activationCode: ")

        car_dict = {"ownerName": ownerName, "serialNumber": serialNumber,
                                                              "modelYear": modelYear, "code": code,
                                                              "vehicleCode": vehicleCode,
                                                              "model": model, "activationCode": activationCode,
                                                              "engine": engine if isinstance(engine, int) else
                                                              {"capacity": engine.capacity,
                                                                         "num_cylinders": engine.num_cylinders,
                                                                         "max_rpm": engine.max_rpm,
                                                                         "manufacturer_code": engine.manufacturer_code},
                                                              "fuelFigures": {"speed": speed, "mpg": mpg,
                                                                              "usageDescription": usageDescription},
                                                              "performanceFigures": {
                                                                  "acceleration": {"mph": acceleration_mph,
                                                                                   "seconds": acceleration_seconds},
                                                                  "octaneRating": octaneRating},
                                                              "manufacturer": manufacturer}
        car_json = json.dumps(car_dict)
        r = requests.post('http://localhost:5000/cars', json=car_json)

        if r.status_code == 201:
            return True
        else:
            return False
    except Exception as ex:
        raise


def get_all_cars():
    r = requests.get("http://localhost:5000/cars")
    res_cars = []
    if r.status_code == 200:
        cars = r.json()["cars"]
        i = 1
        if len(cars) == 0:
            print("--- No cars found ---")
        for c in cars:
            # car = CarController.car_decode(json.loads(c))
            car = json.loads(c)
            print("--- {} ---".format(i))
            print_car(car)
            i += 1
        return True
    else:
        raise Exception('Cannot fetch all tasks: {}'.format(r.status_code))


def print_car(car):
    engine = get_engine(car["engine"])
    ff = get_fuel_figues(car["fuelFigures"])
    pf = get_perf_figures(car["fuelFigures"])
    print("ownerName: {}".format(car["owner_name"]))
    print("serialNumber: {}".format(car["serial_number"]))
    print("modelYear: {}".format(car["model_year"]))
    print("code: {}".format(car["code"]))
    print("vehicleCode: {}".format(car["vehicle_code"]))
    print("engine:")
    print("   capacity: {}".format(engine["capacity"]))
    print("   numCylinders: {}".format(engine["num_cylinders"]))
    print("   maxRpm: {}".format(engine["max_rpm"]))
    print("   manufacturerCode: {}".format(engine["manufacturer_code"]))
    print("fuelFigures:")
    print("   speed: {}".format(ff["speed"]))
    print("   mpg: {}".format(ff["mpg"]))
    print("   usageDescription: {}".format(ff["usageDescription"]))
    print("performanceFigures:")
    print("   octaneRating: {}".format(pf["octaneRating"]))
    print("   acceleration, mph: {}".format(pf["acceleration"][0]))
    print("   acceleration, seconds: {}".format(pf["acceleration"][1]))
    print("manufacturer: {}".format(car["manufacturer"]))
    print("model: {}".format(car["model"]))
    print("activationCode: {}".format(car["activationCode"]))
    print("---")


def get_car_by_id(id):
    r = requests.get("http://localhost:5000/cars/{}".format(id))
    if r.status_code == 200:
        print_car(r.json())
        return True
    else:
        raise Exception("Cannot fetch car #{}: http status {}".format(id, r.status_code))


def delete_car_by_id(id):
    r = requests.delete("http://localhost:5000/cars/{}".format(id))
    if r.status_code == 200:
        return True
    else:
        raise Exception("Could not delete car #{}: http status {}".format(id, r.status_code))

if __name__ == "__main__":
    main()
