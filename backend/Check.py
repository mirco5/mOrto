import abc
from gpiozero import LED
import time
from enum import Enum
import threading
from abc import ABCMeta, abstractmethod
import six
from Device import devices

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