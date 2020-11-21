import time

from sensor import Sensor

class MainLoop:
    i=0
    sensors = dict()

    def __init__(self, tick):
        self.tick = tick
    
    def init(self):
        print("Init Started")
        fh = open("sensorList.csv", "r")
        while True:
            line = fh.readline()
            if not line:
                break
            tokens = line.split(";")
            MainLoop.sensors[tokens[0]] = Sensor(tokens[0],tokens[1].replace("\n",""))  
        fh.close()
        print("Init Finished")

    def run(self):
        print("Main Loop Started")
        while True:
            startTime = time.time()

            # Do Something
            MainLoop.i +=1
            print(MainLoop.i)

            # Start Compute Time
            endTime = time.time()
            remainingTime = endTime - startTime
            time.sleep(self.tick - remainingTime)
            # End Compute Time

         


