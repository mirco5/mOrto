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
from Check import Threshould, EmergencyThreshould, OnceADay, ActivationTime, NoActivationPeriod
from datetime import date, time, datetime

flask_app = Flask(__name__)
app = Api(app = flask_app)
generalns = app.namespace('general')
devicesns = app.namespace('devices')
recipesns = app.namespace('recipes')
checksns = app.namespace('checks')

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
        
        current=[]
        for x in devices:
            actualDevice = DeviceDTO(devices[x].name, devices[x].requestedStatus, devices[x].status, devices[x].typ, devices[x].pins)
            current.append(actualDevice.__dict__)
        jsonToSave=json.dumps(current, indent=4, sort_keys=True)
        
        text_file = open("Devices.json", "w")
        text_file.write(jsonToSave)
        text_file.close()

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
            recipesToReturn.append(recipes[x].name)
        exitval = json.dumps(recipesToReturn)
        return exitval, 200, {'ContentType':'application/json'} 

@recipesns.route('/<recipekey>')
class recipe_key(Resource):
    def get(self,recipekey):
        global recipes
        current = RecipeDTO(recipes[recipekey].name, recipes[recipekey].description, recipes[recipekey].recipeDevices, recipes[recipekey].frequency, recipes[recipekey].duration, recipes[recipekey].checks)
        exitval = json.dumps(current.__dict__, default=lambda o: getattr(o, '__dict__', str(o)))
        return exitval, 200, {'ContentType':'application/json'} 
    def delete(self,recipekey):
        global recipes
        del recipes[recipekey]
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def updateRecipePersistance():
    current=[]
    for x in recipes:
        actualRecipe = RecipeDTO(recipes[x].name, recipes[x].description, recipes[x].recipeDevices, recipes[x].frequency, recipes[x].duration, recipes[x].checks)
        current.append(actualRecipe.__dict__)
    jsonToSave=json.dumps(current, default=lambda o: getattr(o, '__dict__', str(o)), indent=4, sort_keys=True) 
    text_file = open("Recipes.json", "w")
    text_file.write(jsonToSave)
    text_file.close()

@recipesns.route('/<recipekey>/<description>/<devices>/<frequency>/<duration>')
class recipe_create(Resource):
    def post(self,recipekey,description,devices,frequency,duration):
        global recipes
        recipes[recipekey] = Recipe(recipekey,description,devices.split("-"),frequency,duration, dict()) 
        updateRecipePersistance()   
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@checksns.route('/treshould/<recipekey>/<checkkey>/<devicekey>/<check>/<treshouldvalue>')
class recipe_treshould_create(Resource):
    def post(self,recipekey,checkkey,devicekey,check,treshouldvalue):
        global recipes
        global devices
        if issubclass(devices[devicekey].__class__, MeterDevice) :
            recipes[recipekey].checks[checkkey] = Threshould("devices['"+devicekey+"'].value",check,treshouldvalue)        
        
        updateRecipePersistance()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@checksns.route('/emergencytreshould/<recipekey>/<checkkey>/<devicekey>/<check>/<treshouldvalue>')
class recipe_emergencytreshould_create(Resource):
    def post(self,recipekey,checkkey,devicekey,check,treshouldvalue):
        global recipes
        global devices
        if issubclass(devices[devicekey].__class__, MeterDevice) :
            recipes[recipekey].checks[checkkey] = EmergencyThreshould("devices['"+devicekey+"'].value",check,treshouldvalue)        
        
        updateRecipePersistance()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@checksns.route('/onceaday/<recipekey>')
class recipe_onceaday_create(Resource):
    def post(self,recipekey):
        global recipes
        global devices
        recipes[recipekey].checks['onceaday'] = OnceADay(recipekey)        
        updateRecipePersistance()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@checksns.route('/activationtime/<recipekey>/<checkkey>/<hours>/<minutes>/<deltasec>')
class recipe_activationtime_create(Resource):
    def post(self,recipekey, checkkey, hours, minutes, deltasec):
        global recipes
        global devices
        recipes[recipekey].checks[checkkey] = ActivationTime(hours, minutes, deltasec)        
        updateRecipePersistance()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@checksns.route('/noactivationperiod/<recipekey>/<checkkey>/<starthours>/<startmin>/<stophours>/<stopmin>/')
class recipe_noactivationperiod_create(Resource):
    def post(self,recipekey, checkkey, starthours, startmin, stophours, stopmin):
        global recipes
        global devices
        recipes[recipekey].checks[checkkey] = NoActivationPeriod(starthours, startmin, stophours, stopmin)        
        updateRecipePersistance()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@recipesns.route('/<recipekey>/active')
class recipe_active(Resource):
    def get(self,recipekey):
        global recipes
        recipes[recipekey].active()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@recipesns.route('/<recipekey>/deactive')
class recipe_deactive(Resource):
    def get(self,recipekey):
        global recipes
        recipes[recipekey].deactive()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 