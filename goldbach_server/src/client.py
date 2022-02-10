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
   
    work = "11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100"
    self.sendMessage(self.server_socket, work)

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
