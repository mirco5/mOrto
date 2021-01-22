import time
import os
from Device import Device, Nozzle, Ultrasonic, TermoMeter, HumidityMeter, TerrainHumidityMeter
from Singleton import Singleton
from Device import devices
from Recipe import recipes
from Recipe import Recipe
import json
from types import SimpleNamespace
from Check import Threshould, OnceADay, EmergencyThreshould, ActivationTime, NoActivationPeriod

class MainLoop:
    global devices
    global recipes
    tickCounter=0
    tick = 1
    threads = []

    def __init__(self, tick):
        self.tick = tick
     
    def init(self):
        fh = open("Devices.json", "r")
        devicesLoaded = json.load(fh) 
        fh.close()

        for val in devicesLoaded:
            if val['typ'] == "nozzle":
                devices[val['name']] = Nozzle(val['name'],val['typ'], val['pins'])  
            elif val['typ'] == "ultrasonic":
                devices[val['name']] = Ultrasonic(val['name'],val['typ'], val['pins']) 
            elif val['typ'] == "termometer":
                devices[val['name']] = TermoMeter(val['name'],val['typ'], val['pins']) 
            elif val['typ'] == "humiditymeter":
                devices[val['name']] = HumidityMeter(val['name'],val['typ'], val['pins']) 
            elif val['typ'] == "terrainhumiditymeter":
                devices[val['name']] = TerrainHumidityMeter(val['name'],val['typ'], val['pins']) 
        
        for x in devices:
            devices[x].init()
            devices[x].status=3
        
        fh = open("Recipes.json", "r")
        recipesLoaded = json.load(fh) 
        fh.close()

        for val in recipesLoaded:
            connectedDevices = []
            for x in  val['recipeDevices']:
                connectedDevices.append(x)
            checks = dict()
            for x,y in val['checks'].items():
                if y['tp'] == "Threshould" :
                    checks[x] = Threshould(y['valueToTest'],y['operator'],y['value'])
                elif y['tp'] == "EmergencyThreshould" :
                    checks[x] = EmergencyThreshould(y['valueToTest'],y['operator'],y['value'])
                elif y['tp'] == "OnceADay" :
                    checks[x] = OnceADay(y['recipeName'])
                elif y['tp'] == "ActivationTime" :
                    checks[x] = ActivationTime(y['hours'], y['minutes'], y['maxDelta'])
                elif y['tp'] == "NoActivationPeriod" :
                    checks[x] = NoActivationPeriod(y['starthours'], y['startmin'], y['stophours'], y['stopmin'])

            recipes[val['name']] = Recipe(val['name'], val['description'], connectedDevices, val['frequency'], val['duration'], checks)  

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

            for x in recipes:
                recipes[x].run()

            # Start Compute Time
            endTime = time.time()
            remainingTime = endTime - startTime
            if Singleton.getInstance().SysTick - remainingTime >0 :
                time.sleep(Singleton.getInstance().SysTick - remainingTime)
            # End Compute Time
