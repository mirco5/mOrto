import time
import os
from Device import Device, Nozzle, Ultrasonic
import Singleton
from FlaskServer import devices

class MainLoop:
    global devices
    tickCounter=0
    tick = 1
    threads = []

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
                devices[tokens[0]] = Nozzle(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))  
            elif tokens[1].lower() == "ultrasonic":
                devices[tokens[0]] = Ultrasonic(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))
        fh.close()
        for x in devices:
            devices[x].init()
            devices[x].status=3
        print("Init Finished")

    def run(self):
        print("Main Loop Started")
        while True:
            startTime = time.time()
            # TO DO CHECK DEVICE STATE AND CHANGE IT
            MainLoop.tickCounter +=1
            print(MainLoop.tickCounter)

            for x in devices:
                if devices[x].requestedStatus != 0 :
                    if devices[x].requestedStatus==2 :
                        devices[x].status=2
                        devices[x].run()
                    if devices[x].requestedStatus==3 :
                        if devices[x].status==2:
                            devices[x].status=3
                            devices[x].stop()
                        if devices[x].status==4:
                            devices[x].status=3
                            devices[x].carryOnTime=0
                    if devices[x].requestedStatus==4 :
                        devices[x].status=4
                        devices[x].carryOn()
                    devices[x].requestedStatus = 0

            # Start Compute Time
            endTime = time.time()
            remainingTime = endTime - startTime
            if Singleton.Singleton.getInstance().SysTick - remainingTime >0 :
                time.sleep(Singleton.Singleton.getInstance().SysTick - remainingTime)
            # End Compute Time
