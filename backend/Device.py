import abc

class Device(metaclass=abc.ABCMeta):
    def __init__(self, name, typ, pins):
        self.__name = name
        self.__typ = typ
        self.__pins = pins

    def setvalue(self, value):
        self.__value=value
    def getvalue(self):
        return self.__value
    def getname(self):
        return self.__name
    def gettyp(self):
        return self.__typ
    def getpins(self):
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

@Device.register
class Nozzle(Device):
    def init(self):
        print("Init Started")
        print("Init Finished")
    def run(self):
        print("Run Started")
        print("Run Finished")
    def stop(self):
        print("Stop Started")
        print("Stop Finished")

@Device.register
class Ultrasonic(Device):
    def init(self):
        print("Init Started")
        print("Init Finished")
    def run(self):
        print("Run Started")
        print("Run Finished")
    def stop(self):
        print("Stop Started")
        print("Stop Finished")
