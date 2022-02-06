import imp
import socket
import os
from time import sleep
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
    self.logAppend('Connecting on %s port %s \n' % SERVER_ADDR)
    self.server_socket.connect(SERVER_ADDR)
    available_threads = os.sysconf("SC_NPROCESSORS_ONLN")
    self.sendMessage(self.server_socket, str(available_threads))

    libGoldbach.main()

  def stop(self):
    self.logAppend("closing sockets...")
    self.server_socket.close()
  
  def sendMessage(self, connection, message):
    message = message.encode("utf-8")
    connection.sendall(message)

  def recvMessage(self, connection):
    message = connection.recv(PACKAGE_SIZE)
    message = message.decode("utf-8")
    return message

  def logAppend(self, message):
    print("\n[CLIENT] "+message)

if __name__ == "__main__":
    client = Client()
