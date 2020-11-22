from multiprocessing import Process
from MainLoop import MainLoop
from FlaskServer import run

if __name__ == '__main__':
  mnlp = MainLoop(1)
  mnlp.init()
  
  p1 = Process(target=mnlp.run)
  p1.start()

  p2 = Process(target=run)
  p2.start()

  p1.join()
  p2.join()