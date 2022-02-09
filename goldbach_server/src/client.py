import ctypes
import socket
import os
from ctypes import *

libGoldbach = CDLL("./bin/libGoldbach.so")

# Protocol defined message size
PACKAGE_SIZE = 1024

# Server info
SERVER_IP = '192.168.1.115'
SERVER_PORT = 5000
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

class Client():
  def __init__(self): 
    # Used for TCP communication with the server
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.logAppend('Connecting on %s port %s ' % SERVER_ADDR)
    self.server_socket.connect(SERVER_ADDR)
    self.sendMessage(self.server_socket, "client")
    while True:
      work = "input 23"
      self.sendMessage(self.server_socket, work)
      if(work == "stop"):
        self.logAppend("closing connection")
        self.sendMessage(self.server_socket, "disconect")
        self.stop()
        break
      else:
        results = self.recvMessage(self.server_socket)
        self.logAppend("Goldbach sums results: \n\n"+results)
        

  def stop(self):
    self.logAppend("closing sockets...")
    self.server_socket.close()
  
  def sendMessage(self, connection, message):
    message = self.fill_with_trash(message, PACKAGE_SIZE)
    connection.sendall(message)

  def recvMessage(self, connection):
      message = connection.recv(PACKAGE_SIZE)
      message = message.decode("utf-8")
      # Clean message thrash
      message = message.replace('$','')
      return message

  def fill_with_trash(self, message, package_size):
    for index in range(package_size-len(message)):
        message += '$'
    return message.encode("utf-8")

  def logAppend(self, message):
    print("\n[CLIENT] "+message)

if __name__ == "__main__":
    client = Client()
