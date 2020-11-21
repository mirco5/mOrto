import os
from flask import Flask
from gpiozero import CPUTemperature
from mainloop import MainLoop


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/temperature')
def hello_name():
    cpu = CPUTemperature()
    return str(cpu.temperature)

if __name__ == '__main__':
    mnlp = MainLoop(1)
    mnlp.init()
    mnlp.run()
    app.run(host= '192.168.1.169')
