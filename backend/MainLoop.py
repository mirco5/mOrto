import time
import os
from Device import Device, Nozzle, Ultrasonic
import Singleton

class MainLoop:
    tickCounter=0
    __devices__ = dict()
    tick = 1

    def __init__(self, tick):
        self.tick = tick
     
    def init(self):
        print("Init Started")
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        fh = open(os.path.join(__location__, "sensorList.csv"), "r")
        while True:
            line = fh.readline()
            if not line:
                break
            tokens = line.split(";")
            if tokens[1].lower() == "nozzle":
                self.__devices__[tokens[0]] = Nozzle(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))  
            elif tokens[1].lower() == "ultrasonic":
                self.__devices__[tokens[0]] = Ultrasonic(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))  

        fh.close()
        for x in self.__devices__:
            self.__devices__[x].init()
        print("Init Finished")

    def run(self):
        print("Main Loop Started")
        while True:
            startTime = time.time()

            # Do Something
            MainLoop.tickCounter +=1
            print(MainLoop.tickCounter)

            # Start Compute Time
            endTime = time.time()
            remainingTime = endTime - startTime
            time.sleep(Singleton.Singleton.getInstance().SysTick - remainingTime)
            # End Compute Time
