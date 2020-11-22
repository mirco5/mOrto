import os
from flask import Flask
from gpiozero import CPUTemperature
from MainLoop import MainLoop

app = Flask(__name__)

def run():
    app.run(host = '192.168.1.169') 

@app.route('/temperature')
def hello_name():
    cpu = CPUTemperature()
    return str(cpu.temperature)

@app.route('/devices/<devicekey>')
def device(devicekey):
    return str(MainLoop.__devices__[devicekey])
