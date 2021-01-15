import abc
from gpiozero import LED
import time
from enum import Enum
import threading
from abc import ABCMeta, abstractmethod
import six
from Device import devices
from Recipe import recipes
import datetime

@six.add_metaclass(abc.ABCMeta)
class Check():
    @abstractmethod
    def run(self):
        pass
    @property
    def typ(self):
        return self.tp
    @typ.setter
    def typ(self, value):
        self.tp=value

@Check.register
class Threshould(Check):
    def __init__(self, valueToTest, operator, value): 
        self.valueToTest = valueToTest
        self.operator = operator
        self.value = value
        self.tp = "Threshould"

    def run(self):
        global devices
        coreCode = str(self.valueToTest) + str(self.operator) + str(self.value)
        evaluation = eval(coreCode, {'devices':devices})
        return evaluation

@Check.register
class OnceADay(Check):
    def __init__(self, recipeName): 
        self.tp = "OnceADay"
        self.recipeName = recipeName
    
    def run(self):
        global recipes
        lastExecDays = time.localtime(recipes[self.recipeName].lastExecFinishTime)
        todayDays = time.localtime(time.time())
        if lastExecDays.tm_yday < todayDays.tm_yday :
            return True
        else:
            return False

@Check.register
class ActivationTime(Check):
    def __init__(self, time, maxDelta): 
        self.tp = "ActivationTime"
        self.time = time
        self.maxDelta = maxDelta

    def run(self):
        currentTime = time.time()
        return currentTime > self.time and (currentTime < (self.time + self.maxDelta))

@Check.register
class NoActivationPeriod(Check):
    def __init__(self, startTime, stopTime): 
        self.tp = "ActivationTime"
        self.startTime = startTime
        self.stopTime = stopTime

    def run(self):
        currentTime = time.time()
        return currentTime < self.startTime and currentTime > self.stopTime

@Check.register
class EmergencyActivation(Check):
    def __init__(self, time, maxDelta): 
        self.tp = "ActivationTime"
        self.time = time
        self.maxDelta = maxDelta

    def run(self):
        currentTime = time.time()
        return currentTime > self.time and (currentTime < (self.time + self.maxDelta))
