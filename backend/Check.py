import abc
from gpiozero import LED
import time
from enum import Enum
import threading
from abc import ABCMeta, abstractmethod
import six

@six.add_metaclass(abc.ABCMeta)
class Check():
    @abstractmethod
    def run(self):
        pass

@Check.register
class Threshould(Check):
    def __init__(self, valueToTest, operator, value): 
        self.__expr = valueToTest+operator+value
    @property
    def run(self):
        return exec(self.__expr)