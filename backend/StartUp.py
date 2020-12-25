from threading import Thread
import time
from FlaskServer import run
from FlaskServer import devices
from MainLoop import MainLoop

if __name__ == '__main__':
  try:  
    mnlp = MainLoop(1)
    mnlp.init()
    
    p1 = Thread(target = mnlp.run)
    p1.start()

    p2 = Thread(target = run)
    p2.start()

    p1.join()
    p2.join()

    for x in devices:
      devices[x].exit()
  except:  
    print("Other error or exception occurred!")
  finally:
    for x in devices:
      devices[x].exit()
