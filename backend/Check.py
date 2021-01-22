import abc
from gpiozero import LED
import time
from enum import Enum
import threading
from abc import ABCMeta, abstractmethod
import six
from Device import devices
from Recipe import recipes
import time

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
class EmergencyThreshould(Check):
    def __init__(self, valueToTest, operator, value): 
        self.valueToTest = valueToTest
        self.operator = operator
        self.value = value
        self.tp = "EmergencyThreshould"

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
    def __init__(self, hours, minutes, maxDelta): 
        self.tp = "ActivationTime"
        self.hours = hours
        self.minutes = minutes
        self.maxDelta = maxDelta

    def run(self):
        currentTime = time.time()
        targetTime = time.time()
        targetTime = targetTime + int(self.hours) * (60*60) + int(self.minutes) * 60
        maxTime = targetTime + int(self.maxDelta)
        return currentTime > targetTime and currentTime < maxTime

@Check.register
class NoActivationPeriod(Check):
    def __init__(self, startHours, stopHours, startMin, stopMin): 
        self.tp = "NoActivationPeriod"
        self.starthours = startHours
        self.stophours = stopHours
        self.startmin = startMin
        self.stopmin = stopMin

    def run(self):
        currentTime = time.time()
        if (currentTime/(60*60)) == int(self.starthours):
            return (currentTime/60) < int(self.startmin)
        else:
            return ((currentTime/(60*60)) < int(self.starthours) and (currentTime/60) < int(self.startmin)) or ((currentTime/(60*60)) > int(self.starthours) and (currentTime/60) > int(self.startmin))