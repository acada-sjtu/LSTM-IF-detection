#FILEPATH = "./Samples/test2.v"
#FILEPATH = "./Samples/c432.v"
FILEPATH = "./Samples/b10.v"
#FILEPATH = "./Samples/test2new.v"
#FILEPATH = "./Samples/4gate.v"
#FILEPATH = "./Samples/b01.v"

import time
from datetime import timedelta
from supervisor import *
import sys
sys.setrecursionlimit(1000000000)
class Main:
  
  def __init__(self):
    self.doQueries()
    
    
  def doQueries(self):
    self.queryFile()
    self.queryModifier()
    self.queryQ()
    
  def queryFile(self):
    #file = input("\nPlease specify the path of a verilog file:\n(Hit ENTER for " + FILEPATH + " )\n\n> ")
    #self.file = file if file != '' else FILEPATH
    self.file = FILEPATH
  def queryModifier(self):
##    modifier = input("\nType in 'O1' for the stuck-at-one flaw, '10' for the stuck-at-zero, or press ENTER not to activate these.\n\n> ")
##    modifier = modifier if modifier != "" else "00"
##    if modifier != "00" and modifier != "01" and modifier != "10":
##      raise ValueError("The modifier must be either '01', either '10' or '00'.")
    modifier = "01"
    self.modifier = modifier

  def queryQ(self):
##    q = input("\nType in the reliability you want for all the gates, or hit ENTER for the default value (0.5).\n\n> ")
##    q = q if q != "" else 0.5
##    try:
##      q = float(q)
##    except ValueError:
##      print("q must be a float")
##    if q < 0 or q > 1:
##      raise ValueError("q must verify 0 <= q <= 1")
    q = 1.0
    self.q = q

  def run(self):
    print("\nPlease wait for the tests to occur.\nIt can take up to several minutes depending on your computer.\n\n")
    supervisor = Supervisor(self.file, self.modifier, self.q)
    startTime = time.time()
    
    supervisor.launch()
    endTime = time.time()
    delta = timedelta(seconds=endTime-startTime)
    message = str(delta.days) + " days" if delta.days > 0 else ( str(delta.seconds) + " seconds" if delta.seconds > 0 else "less than a second" )
    print("The computation took " + message + ".")
   
    
Main().run()
