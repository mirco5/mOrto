import time
import os
from Device import Device, Nozzle, Ultrasonic

class MainLoop:
    tickCounter=0
    __devices__ = dict()

    def getname(self):
        return self.__devices__

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
            # To do differentiate devices
            self.__devices__[tokens[0]] = Ultrasonic(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))  
        fh.close()

        for x in self.__devices__:
            x.init()
            
        # To do start sensors

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
            time.sleep(self.tick - remainingTime)
            # End Compute Time
