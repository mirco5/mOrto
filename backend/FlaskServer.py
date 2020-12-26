import os
from flask import Flask
from gpiozero import CPUTemperature
import json
from Recipe import Recipe
from Recipe import recipes
from Device import devices

app = Flask(__name__)

def run():
    app.run(host = '192.168.1.169') 

@app.route('/temperature')
def temperature():
    cpu = CPUTemperature()
    return str(cpu.temperature)

@app.route('/devices/<devicekey>')
def device(devicekey):
    global devices
    return json.dumps(devices[devicekey].__dict__)

@app.route('/devices/<devicekey>/run')
def device_run(devicekey):
    global devices
    devices[devicekey].requestedStatus=int(2)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/devices/<devicekey>/stop')
def device_stop(devicekey):
    global devices
    devices[devicekey].requestedStatus=int(3)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/devices/<devicekey>/carryOn/<time>/<tick>')
def device_carryOn(devicekey, time, tick):
    global devices
    devices[devicekey].requestedStatus = int(4)
    devices[devicekey].carryOnTime = float(time)
    devices[devicekey].carryOnTick = float(tick)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/recipe/<recipekey>')
def recipe(recipekey):
    global devices
    return json.dumps(devices[recipekey].__dict__)

@app.route('/recipe/<recipekey>/<description>/<devices>/<frequency>/<duration>')
def recipe_create(recipekey,description,devices,frequency,duration):
    recipes[recipekey] = Recipe(recipekey,description,devices,frequency,duration) 
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
