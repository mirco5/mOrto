import os
from flask import Flask, jsonify
from flask_restplus import Api, Resource
from gpiozero import CPUTemperature
import json
from Recipe import Recipe, RecipeDTO, recipes
from Device import devices
from Device import DeviceDTO
from Device import MeterDevice
from Device import Device, Nozzle, Ultrasonic, TermoMeter, HumidityMeter, TerrainHumidityMeter


flask_app = Flask(__name__)
app = Api(app = flask_app)
generalns = app.namespace('general')
devicesns = app.namespace('devices')
recipesns = app.namespace('recipes')

def run():
    flask_app.run(host = '192.168.1.169')

@generalns.route('/temperature')
class temperature(Resource):
    def get(self):
        cpu = CPUTemperature()
        return json.dumps(cpu.temperature), 200, {'ContentType':'application/json'} 

@devicesns.route('/')
class device_list(Resource):
    def get(self):
        global devices
        devicesToReturn=[]
        for x in devices:
            current = DeviceDTO(devices[x].name, devices[x].requestedStatus, devices[x].status, devices[x].typ, devices[x].pins)
            if issubclass(devices[x].__class__, MeterDevice) :
                current.value = devices[x].value
            devicesToReturn.append(current.name)
        exitval = json.dumps(devicesToReturn)
        return exitval, 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>')
class device_devicekey(Resource):
    def get(self,devicekey):
        global devices
        current = DeviceDTO(devices[devicekey].name, devices[devicekey].requestedStatus, devices[devicekey].status, devices[devicekey].typ, devices[devicekey].pins)
        if issubclass(devices[devicekey].__class__, MeterDevice) :
            current.value = devices[devicekey].value
        exitval = json.dumps(current.__dict__)
        return exitval, 200, {'ContentType':'application/json'}

    def delete(self,devicekey):
        global devices
        del devices[devicekey]
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>/<typ>/<pins>')
class device_adddevice(Resource):
    def post(self,devicekey,typ,pins):
        global devices
        if typ.lower() == "nozzle":
            devices[devicekey] = Nozzle(devicekey, typ, pins.split("-"))  
        elif typ.lower() == "ultrasonic":
            devices[devicekey] = Ultrasonic(devicekey, typ, pins.split("-"))
        elif typ.lower() == "termometer":
            devices[devicekey] = TermoMeter(devicekey, typ, pins.split("-"))
        elif typ.lower() == "humiditymeter":
            devices[devicekey] = HumidityMeter(devicekey, typ, pins.split("-"))
        elif typ.lower() == "terrainhumiditymeter":
            devices[devicekey] = TerrainHumidityMeter(devicekey, typ, pins.split("-"))
        #TODO:Save current view
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>/status/run')
class device_run(Resource):
    def get(self,devicekey):
        global devices
        devices[devicekey].requestedStatus=int(2)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>/status/stop')
class device_stop(Resource):
    def get(self,devicekey):
        global devices
        devices[devicekey].requestedStatus=int(3)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>/status/carryOn/<time>/<tick>')
class device_carryOn(Resource):
    def get(self,devicekey, time, tick):
        global devices
        devices[devicekey].requestedStatus = int(4)
        devices[devicekey].carryOnTime = float(time)
        devices[devicekey].carryOnTick = float(tick)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@recipesns.route('/')
class recipe_list(Resource):
    def get(self):
        global recipes
        recipesToReturn=[]
        for x in recipes:
            current = RecipeDTO(recipes[x].name, recipes[x].description, recipes[x].recipeDevices, recipes[x].frequency, recipes[x].duration)
            recipesToReturn.append(current.name)
        exitval = json.dumps(recipesToReturn)
        return exitval, 200, {'ContentType':'application/json'} 

@recipesns.route('/<recipekey>')
class recipe_key(Resource):
    def get(self,recipekey):
        global recipes
        current = RecipeDTO(recipes[recipekey].name, recipes[recipekey].description, recipes[recipekey].recipeDevices, recipes[recipekey].frequency, recipes[recipekey].duration)
        exitval = json.dumps(current.__dict__)
        return exitval, 200, {'ContentType':'application/json'} 
    def delete(self,recipekey):
        global recipes
        del recipes[recipekey]
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@recipesns.route('/<recipekey>/<description>/<devices>/<frequency>/<duration>')
class recipe_create(Resource):
    def post(self,recipekey,description,devices,frequency,duration):
        global recipes
        recipes[recipekey] = Recipe(recipekey,description,devices.split("-"),frequency,duration) 
        #TODO:Save current view
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}