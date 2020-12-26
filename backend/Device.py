import abc
from gpiozero import LED
import json
import time
import sys
import MainLoop
import Singleton
from enum import Enum
import threading
from abc import ABCMeta, abstractmethod

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(name=fn, target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

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
    @property    
    @abstractmethod
    def init(self):
        pass
    @property    
    @abstractmethod
    def run(self):
        pass
    @property    
    @abstractmethod
    def stop(self):
        pass
    @threaded
    def carryOn(self):
        self.status = 4
        startTime = time.time()
        currentTick = self.carryOnTick
        if currentTick==None or currentTick == 0:
            currentTick = Singleton.Singleton.getInstance().SysTick
        time.time()
        while self.carryOnTime != 0 and (time.time() - startTime) < self.carryOnTime:
            endTime = time.time()
            self.run()
            endTime = endTime - time.time()
            sleepTime = currentTick - endTime
            if sleepTime > 0:
                time.sleep(sleepTime)
        self.stop()
    @property    
    @abstractmethod
    def exit(self):      
        pass

@Device.register
class Nozzle(Device):
    @property
    def obit(self):
        return self.__obit
    @threaded
    def init(self):
        self.__obit = LED(int(self.pins[0]))
        print("Init Finished:" + self.name)
    @threaded
    def run(self):
        self.__obit.on()
    @threaded
    def stop(self):
        self.__obit.off()
        print("Stop Finished:" + self.name)
    @threaded
    def exit(self):
        self.__obit.close()
        print("Exit Finished:" + self.name)

@Device.register
class Ultrasonic(Device):
    @threaded
    def init(self):
        print("Init Finished:" + self.name)
    @threaded
    def run(self):
        print("Run:" + self.name)
    @threaded
    def stop(self):
        print("Stop Finished:" + self.name)
    @threaded
    def exit(self):
        print("Exit Finished:" + self.name)    
