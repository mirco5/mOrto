import time
import os
from Device import Device, Nozzle, Ultrasonic, TermoMeter, HumidityMeter, TerrainHumidityMeter
from Singleton import Singleton
from Device import devices
from Recipe import recipes
from Recipe import Recipe

class MainLoop:
    global devices
    global recipes
    tickCounter=0
    tick = 1
    threads = []

    def __init__(self, tick):
        self.tick = tick
     
    def init(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        fh = open(os.path.join(__location__, "./configFiles/sensorList.csv"), "r")
        while True:
            line = fh.readline()
            if not line:
                break
            tokens = line.split(";")
            if tokens[1].lower() == "nozzle":
                devices[tokens[0]] = Nozzle(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))  
            elif tokens[1].lower() == "ultrasonic":
                devices[tokens[0]] = Ultrasonic(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))
            elif tokens[1].lower() == "termometer":
                devices[tokens[0]] = TermoMeter(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))
            elif tokens[1].lower() == "humiditymeter":
                devices[tokens[0]] = HumidityMeter(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))
            elif tokens[1].lower() == "terrainhumiditymeter":
                devices[tokens[0]] = TerrainHumidityMeter(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","))
        fh.close()
        for x in devices:
            devices[x].init()
            devices[x].status=3
        
        fh = open(os.path.join(__location__, "./configFiles/recipesList.csv"), "r")
        while True:
            line = fh.readline()
            if not line:
                break
            tokens = line.split(";")
            if tokens[1].lower() == "nozzle":
                recipes[tokens[0]] = Recipe(tokens[0],tokens[1].replace("\n",""), tokens[2].replace("\n","").split(","), tokens[3].replace("\n",""), tokens[4].replace("\n","")) 
        fh.close()

    def run(self):
        print("Main Loop Started")
        while True:
            startTime = time.time()

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
            if Singleton.getInstance().SysTick - remainingTime >0 :
                time.sleep(Singleton.getInstance().SysTick - remainingTime)
            # End Compute Time
