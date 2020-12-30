import os
from flask import Flask
from flask_restplus import Api, Resource
# from flask_swagger_ui import get_swaggerui_blueprint
from gpiozero import CPUTemperature
import json
from Recipe import Recipe
from Recipe import recipes
from Device import devices

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
        return str(cpu.temperature)

@devicesns.route('/<devicekey>')
class device(Resource):
    def get(self,devicekey):
        global devices
        return json.dumps(devices[devicekey].__dict__)

@devicesns.route('/<devicekey>/run')
class device_run(Resource):
    def get(self,devicekey):
        global devices
        devices[devicekey].requestedStatus=int(2)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>/stop')
class device_stop(Resource):
    def get(self,devicekey):
        global devices
        devices[devicekey].requestedStatus=int(3)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@devicesns.route('/<devicekey>/carryOn/<time>/<tick>')
class device_carryOn(Resource):
    def get(self,devicekey, time, tick):
        global devices
        devices[devicekey].requestedStatus = int(4)
        devices[devicekey].carryOnTime = float(time)
        devices[devicekey].carryOnTick = float(tick)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@recipesns.route('/<recipekey>')
class recipe(Resource):
    def get(self,recipekey):
        global devices
        return json.dumps(devices[recipekey].__dict__)

@recipesns.route('/<recipekey>/<description>/<devices>/<frequency>/<duration>')
class recipe_create(Resource):
    def post(self,recipekey,description,devices,frequency,duration):
        recipes[recipekey] = Recipe(recipekey,description,devices,frequency,duration) 
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
