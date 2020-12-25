import abc
from gpiozero import LED
import json
import time
import sys
import MainLoop
import Singleton
from enum import Enum

class Device(metaclass=abc.ABCMeta):
    status = 0
    requestedStatus = 0
    carryOnTick = 0
    carryOnTime = 0

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
    def init(self):
        status = 1
    def run(self):  
        status = 2
    def stop(self):      
        status = 3
    def carryOn(self):
        status = 4
        startTime = time.time()
        currentTick = self.carryOnTick
        if currentTick==None or currentTick == 0:
            currentTick = Singleton.Singleton.getInstance().SysTick
        time.time()
        while (time.time() - startTime) < self.carryOnTime:
            endTime = time.time()
            self.run()
            endTime = endTime - time.time()
            sleepTime = currentTick - endTime
            if sleepTime > 0:
                time.sleep(sleepTime)
        self.stop()
    def exit(self):      
        "Function that exit the sensor"

@Device.register
class Nozzle(Device):
    @property
    def obit(self):
        return self.__obit
    def init(self):
        super().init()
        self.__obit = LED(int(self.pins[0]))
        print("Init Finished:" + self.name)
    def run(self):
        super().run()
        self.__obit.on()
    def stop(self):
        super().stop()
        self.__obit.off()
        print("Stop Finished:" + self.name)
    def exit(self):
        super().exit()
        self.__obit.close()
        print("Exit Finished:" + self.name)

@Device.register
class Ultrasonic(Device):
    def init(self):
        super().init()
        print("Init Finished:" + self.name)
    def run(self):
        super().run()
        print("Run:" + self.name)
    def stop(self):
        super().stop()
        print("Stop Finished:" + self.name)
    def exit(self):
        super.exit()
        print("Exit Finished:" + self.name)    
