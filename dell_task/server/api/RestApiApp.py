import json

from peewee import SqliteDatabase

from flask import Flask, make_response, jsonify, abort, request

from common.Controllers import Controllers
from common.Models import Builder

app = Flask(__name__)


@app.route('/')
def index():
    return "HELLO"


@app.route("/cars", methods=["GET"])
def get_cars():
    res = Controllers.CarController.get_cars()
    if len(res) == 0:
        return jsonify({"cars": []})
    return jsonify({"cars": [json.dumps(x.__dict__["__data__"]) for x in res]})


@app.route("/cars/<int:id>", methods=["GET"])
def get_car(id):
    try:
        res = Controllers.CarController.get_car(id)
        return jsonify(res.__dict__["__data__"])
    except:
        abort(404)


@app.route("/cars", methods=["POST"])
def add_car():
    if not request.json and not request.data:
        abort(400)

    engine = None
    ff = None
    pf = None
    car = None
    try:
        if isinstance(request.json, str):
            car_info = json.loads(request.json)
        else:
            car_info = request.json
        engine = Controllers.CarController.engine_decode(car_info["engine"])
        ff = Controllers.CarController.fuel_figures_decode(car_info["fuelFigures"])
        pf = Controllers.CarController.performance_figures_decode(car_info["performanceFigures"])
        car = Controllers.CarController.add_car(Builder.build_car(owner_name=car_info["ownerName"],
                                                                  serial_number=car_info["serialNumber"],
                                                                  model_year=car_info["modelYear"],
                                                                  code=car_info["code"],
                                                                  vehicle_code=car_info["vehicleCode"],
                                                                  engine=engine,
                                                                  manufacturer=car_info["manufacturer"],
                                                                  fuelFigures=ff,
                                                                  performanceFigures=pf, model=car_info["model"],
                                                                  activationCode=car_info["activationCode"]))

    except AttributeError as ex:
        abort(400, ex)
    except Exception as ex:
        abort(500, ex)
    return jsonify({'car': json.dumps(str(car.__dict__["__data__"]))}), 201


@app.route("/cars/<int:id>", methods=["DELETE"])
def delete_car(id):
    try:
        Controllers.CarController.delete_car(id)
        return jsonify({'result': True}), 200
    except AttributeError as ex:
        abort(400, ex)
    except:
        abort(500)


@app.route("/engines", methods=["GET"])
def get_engines():
    res = Controllers.CarController.get_engines()
    if len(res) == 0:
        return jsonify({"engines": []})
    return jsonify({"engines": [json.dumps(x.__dict__["__data__"]) for x in res]}), 200


@app.route("/engines/<int:id>", methods=["GET"])
def get_engine(id):
    try:
        res = Controllers.CarController.get_engine(id)
        return jsonify({'engine': json.dumps(res.__dict__["__data__"])}), 200
    except Exception as ex:
        abort(404)


@app.route("/fuelFigures/<int:id>", methods=["GET"])
def get_fuel_figures(id):
    try:
        res = Controllers.CarController.get_fuel_figures(id)
        return jsonify({'fuelFigures': json.dumps(res.__dict__["__data__"])}), 200
    except Exception as ex:
        abort(404)


@app.route("/performanceFigures/<int:id>", methods=["GET"])
def get_performance_figures(id):
    try:
        res = Controllers.CarController.get_performance_figures(id)
        return jsonify({'performanceFigures': json.dumps(res.__dict__["__data__"])}), 200
    except Exception as ex:
        abort(404)


@app.route("/engines", methods=["POST"])
def add_engine():
    if not request.json:
        abort(400)
    try:
        engine = Controllers.CarController.add_engine(Builder.build_engine(capacity=request.json["capacity"],
                                                                           num_cylinders=request.json["num_cylinders"],
                                                                           max_rpm=request.json["max_rpm"],
                                                                           manufacturer_code=request.json[
                                                                               "manufacturer_code"]))
        return jsonify({'engine': json.dumps(str(engine.__dict__["__data__"]))}), 201
    except:
        abort(400)


@app.route("/engines/<int:id>", methods=["PUT"])
def update_engine(id):
    if not request.json:
        abort(400)

    engine = Builder.build_engine(capacity=request.json["capacity"],
                                  num_cylinders=request.json["num_cylinders"],
                                  max_rpm=request.json["max_rpm"],
                                  manufacturer_code=request.json["manufacturer_code"])

    try:
        Controllers.CarController.update_engine(engine, id)
        return jsonify({'engine': json.dumps(str(engine.__dict__["__data__"]))}), 201
    except AttributeError as ex:
        abort(404)
    except Exception as ex:
        abort(500)


@app.route("/engines/<int:id>", methods=["DELETE"])
def delete_engine(id):
    try:
        Controllers.CarController.delete_engine(id)
        return jsonify({'result': True})
    except AttributeError as ex:
        abort(404)
    except:
        abort(500)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    Controllers.CarController.init_database(SqliteDatabase('cars.db'))
    app.run(debug=True)

if __name__ == "__main__":
    main()
