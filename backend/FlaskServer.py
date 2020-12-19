import os
from flask import Flask
from gpiozero import CPUTemperature
from MainLoop import MainLoop
import json

app = Flask(__name__)

def run():
    app.run(host = '192.168.1.169') 

@app.route('/temperature')
def hello_name():
    cpu = CPUTemperature()
    return str(cpu.temperature)

@app.route('/devices/<devicekey>')
def device(devicekey):
    return json.dumps(MainLoop.__devices__[devicekey].__dict__)

@app.route('/devices/<devicekey>/run')
def device_run(devicekey):
    return json.dumps(MainLoop.__devices__[devicekey].run())

@app.route('/devices/<devicekey>/stop')
def device_stop(devicekey):
    return json.dumps(MainLoop.__devices__[devicekey].stop())

@app.route('/devices/<devicekey>/carryOn/<time>')
def device_carryOn(devicekey, time):
    return json.dumps(MainLoop.__devices__[devicekey].carryOn(int(time)))

