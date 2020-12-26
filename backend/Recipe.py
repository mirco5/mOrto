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
import six
from FlaskServer import devices
 

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(name=fn, target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Recipe():
    __checks=[]
    def __init__(self, name, description, deviceslist, frequency, duration):
        global devices
        self.__name = name
        self.__description = description
        self.__recipeDevices = dict()
        for x in deviceslist:
           self.__recipeDevices[x] = devices[x]
        self.__frequency = frequency
        self.__duration = duration

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        self.__status=status
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name=name
    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, description):
        self.__description=description
    @property
    def devices(self):
        return self.__recipeDevices
    @property
    def frequency(self):
        return self.__frequency
    @frequency.setter
    def frequency(self, frequency):
        self.__frequency=frequency
    @property
    def duration(self):
        return self.__duration
    @duration.setter
    def duration(self, duration):
        self.__duration=duration    
    @property
    def checks(self):
        return self.__checks  
    @property    
    def active(self):
        self.status = 1
    @property    
    def deactive(self):
        self.status = 0
    @property    
    def enable(self):
        checks = 0
        for x in self.__checks:
            if not self.__checks[x].run():
                checks = 1
        for x in self.__recipeDevices:
            if self.__recipeDevices[x].typ == "nozzle" and checks == 0:
                self.__recipeDevices[x].requestedStatus = 2
    @property    
    def disable(self):
        for x in self.__recipeDevices:
            if self.__recipeDevices[x].typ == "nozzle":
                self.__recipeDevices[x].requestedStatus = 3
    @property    
    def run(self):
        #TO DO Checks on run
        pass
