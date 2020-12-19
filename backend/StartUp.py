from multiprocessing import Process
from MainLoop import MainLoop
from FlaskServer import run
import time

if __name__ == '__main__':
  try:  
    mnlp = MainLoop(1)
    mnlp.init()
    
    p1 = Process(target=mnlp.run)
    p1.start()

    p2 = Process(target=run)
    p2.start()

    p1.join()
    p2.join()
    for x in MainLoop.__devices__:
      MainLoop.__devices__[x].exit()
  except:  
    print("Other error or exception occurred!")
  finally:
    for x in MainLoop.__devices__:
      MainLoop.__devices__[x].exit()
