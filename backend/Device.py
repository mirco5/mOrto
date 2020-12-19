import abc
from gpiozero import LED
import json
import time
import sys
import MainLoop
import Singleton

class Device(metaclass=abc.ABCMeta):
    def __init__(self, name, typ, pins):
        self.__name = name
        self.__typ = typ
        self.__pins = pins
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value):
        self.__value=value
    @property
    def name(self):
        return self.__name
    @property
    def typ(self):
        return self.__typ
    @property
    def pins(self):
        return self.__pins
    @abc.abstractmethod
    def init(self):
        "Function that configure the sensor"
    @abc.abstractmethod
    def run(self):  
        "Function that start the sensor"
    @abc.abstractmethod
    def stop(self):      
        "Function that stop the sensor"
    def carryOn(self, extime, *args, **kwargs):
        forcedTick = kwargs.get('tick', None)
        startTime = time.time()
        if forcedTick is not None:
            currentTick = forcedTick
        else:
            currentTick = Singleton.Singleton.getInstance().SysTick
        while (time.time() - startTime) < extime:
            endTime = time.time()
            self.run()
            endTime= endTime - time.time()
            sleepTime = currentTick - endTime
            if sleepTime > 0 :
                time.sleep(sleepTime)
        self.stop()
    @abc.abstractmethod
    def exit(self):      
        "Function that exit the sensor"

@Device.register
class Nozzle(Device):
    @property
    def obit(self):
        return self.__obit
    def init(self):
        self.__obit = LED(int(self.pins[0]))
        print("Init Finished:" + self.name)
    def run(self):
        print("Run:" + self.name)
        self.__obit.on()
    def stop(self):
        print("Stop Started:" + self.name)
        self.__obit.off()
        print("Stop Finished:" + self.name)
    def exit(self):
        print("Exit Started:" + self.name)
        self.__obit.close()
        print("Exit Finished:" + self.name)

@Device.register
class Ultrasonic(Device):
    def init(self):
        print("Init Finished:" + self.name)
    def run(self):
        print("Run:" + self.name)
    def stop(self):
        print("Stop Started:" + self.name)
        print("Stop Finished:" + self.name)
    def exit(self):
        print("Exit Started:" + self.name)
        print("Exit Finished:" + self.name)    
