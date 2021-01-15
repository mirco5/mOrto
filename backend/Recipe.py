import json
import time
from Device import devices
import threading

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(name=fn, target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

recipes = dict()

class RecipeDTO():
    def __init__(self, name, description, recipeDevicesString, frequency, duration, checks):
        global devices
        self.name = name
        self.description = description
        self.recipeDevices = dict()
        for x in recipeDevicesString:
           self.recipeDevices[x] = recipeDevicesString[x].name
        self.frequency = int(frequency)
        self.duration = int(duration)
        self.checks = checks    

class Recipe():
    def __init__(self, name, description, recipeDevicesString, frequency, duration, checks):
        global devices
        self.__name = name
        self.__description = description
        self.__recipeDevices = dict()
        for x in recipeDevicesString:
           self.__recipeDevices[x] = devices[x]
        self.__frequency = int(frequency)
        self.__duration = int(duration)
        self.__checks = checks
        self.__status = 0
        self.__frequencyCounter = -1
        self.__durationCounter = -1
        self.__irrigateState = 1
        self.__lastExec = -1
        self.__lastExecFinishTime=-1

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        self.__status=status
    @property
    def lastExecFinishTime(self):
        return self.__lastExecFinishTime
    @lastExecFinishTime.setter
    def lastExecFinishTime(self, lastExecFinishTime):
        self.__lastExecFinishTime=lastExecFinishTime
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
    def recipeDevices(self):
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
    def active(self):
        self.__status = 1
    def deactive(self):
        self.__status = 0

    def checkPreconditions(self):
        checks = 0
        for x in self.__checks:
            checkResult = self.__checks[x].run()
            if not checkResult:
                checks = 1
        

        if self.__frequencyCounter == -1 :
            self.__frequencyCounter = time.time()
        else:
            currentDeltaTime = time.time() - self.__frequencyCounter
            if self.__status == 1 and currentDeltaTime > self.__frequency :
                self.__irrigateState = 0
                self.__frequencyCounter = -1
                self.__durationCounter = -1
                self.__lastExec =  time.time()
        
        if self.__irrigateState == 0 :
            if self.__durationCounter == -1:
                self.__durationCounter = time.time()
            else:
                currentDeltaDurationTime = time.time() - self.__durationCounter
                if currentDeltaDurationTime > self.__duration :
                    self.__irrigateState = 1
                    self.__durationCounter = -1
                    self.__lastExecFinishTime=time.time()

        if checks == 0 and self.__irrigateState == 0:
            return 0
        else:
            return 1

    def enableNozzles(self):
        for x in self.__recipeDevices:
            if self.__recipeDevices[x].typ == "nozzle" :
                self.__recipeDevices[x].requestedStatus = 2
    def disableNozzles(self):
        for x in self.__recipeDevices:
            if self.__recipeDevices[x].typ == "nozzle":
                self.__recipeDevices[x].requestedStatus = 3
    @threaded
    def run(self):
        if self.__status != 0:
            isToEnable = self.checkPreconditions()
            if  isToEnable == 0:
                self.enableNozzles()
                self.__status = 2
            elif self.__status == 2 and isToEnable !=0 :
                self.disableNozzles()
                self.__status = 1
