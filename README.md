# dell_cars
# This is a simple server-client application for car-vendor.
# New cars can be added to the system, fetched and deleted.
# There are to ways it can be done:
# * using browser to send requests to REST api server
# * using small console application
# To install the dell_cars application you will need python >= 3.4 and pip.
#
# --- Installation ---
# * open a command line prompt
# * navigate to the folder where setup.py resides
# * enter the following command:
# >pip install .
# * once the installation is done, you can see the dell_cars in the list of installed packages:
# >pip list
# or
# >pip show dell_cars
# 
# --- Start application ---
# To start server:
# open a command line prompt
# enger the following command:
# >dell_start_server
# the flask REST api server will be started. Do not close the command line prompt if the server is going to be used.
# To start the client:
# open a command line prompt
# enter the following command:
# >dell_start_client
#
# --- The list of most important rest endpoints ---
# GET: http://localhost:5000/cars - get the list of all cars
# GET: http://localhost:5000/cars/<id> - get the car by #id
# POST: http://localhost:5000/cars - add new car
#  Example json: 
#  {"ownerName":"Jonathan", "serialNumber":1005, "modelYear":2015, "code": "1005", "vehicleCode":"1005", "manufacturer":"Ford", 
#  "engine":
#  {"capacity":5, "num_cylinders": 4, "max_rpm": 5000, "manufacturer_code":"f", "model":"focus", "activationCode":"test_code"},
#  "fuelFigures":
#  {"speed":150, "mpg":15.5, "usageDescription":"test desc"}, 
#  "performanceFigures":
#  {"octaneRating":100, "acceleration""":
#      {"""mph""":160, """seconds""":10.5}}}"
# DELETE: http://localhost:5000/cars/<id> - delete the car by id
