import socket
import os
from ctypes import *
import helpers as Helpers
libGoldbach = CDLL("./goldbach/bin/lib_goldbach_pthread.so")
# libGoldbach = CDLL("./goldbach/bin/lib_goldbach_omp.so")
# libGoldbach = CDLL("./goldbach/bin/lib_goldbach_serial.so")

class Worker():
  def __init__(self):
    self.server_address = (Helpers.SERVER_IP, Helpers.WELCOME_PORT)
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.logAppend('Connecting on %s port %s \n' % self.server_address)

  def start(self):
    self.server_socket.connect(self.server_address)
    Helpers.sendWebMessage("worker", self.server_socket)
    while True:
      work = Helpers.recvWebMessage(self.server_socket)
      if work == '':
        self.stop()
        break
      else:
        libGoldbach.controller_run(int(work)) 
        response = self.readGoldbachResult()
        self.logAppend(response)
        Helpers.sendWorkerMessage(self.server_socket, response)

  def stop(self):
    self.logAppend("closing sockets...")
    self.server_socket.close()

  def logAppend(self, message):
    print("[Worker] "+message)

  def readGoldbachResult(self):
    result = ""
    file = open('Output.txt','r')
    lines = file.readlines()
    for line in lines:
      result+= line
    os.remove("Output.txt")
    return result

if __name__ == "__main__":
  client = Worker()
  client.start()
