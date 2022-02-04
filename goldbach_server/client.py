from encodings import utf_8
import socket

# Server info
SERVER_IP = '192.168.1.115'
SERVER_PORT = 5000
SERVER_ADDR = (SERVER_IP, SERVER_PORT)


class Client():
  def __init__(self): 
    # Used for TCP communication with the server
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('\n[Client] Connection on %s port %s \n' % SERVER_ADDR)
    self.serverSocket.connect(SERVER_ADDR)
    msj = self.serverSocket.recv(1024)
    msj = "client say Hi "
    self.serverSocket.sendall(msj.encode("utf-8"))
    print(msj)

  def stop(self):
    print("closing sockets...")
    self.serverSocket.close()

if __name__ == "__main__":
    client = Client()
