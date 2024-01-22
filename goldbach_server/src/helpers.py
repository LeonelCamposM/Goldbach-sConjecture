import socket

# Server info
# TODO update address
SERVER_IP = '172.30.56.252'
WELCOME_PORT = 5000
PACKAGE_SIZE = 1024

# Api Server info
API_PORT = 8001

# len(message) < PACKAGE_SIZE
# Send data to web client or worker
def sendWebMessage(message, connection):
    message = message.encode("utf_8")
    connection.sendall(message)

def recvWebMessage(connection):
    message = connection.recv(PACKAGE_SIZE)
    message = message.decode("utf-8")
    return message

# Fills the message with trash to avoid message concatenation
def fill_with_trash(message):
    for index in range(PACKAGE_SIZE-len(message)):
        message += '$'
    return message

# len(message) > PACKAGE_SIZE
# Send big messages, usually in n parts
def sendWorkerMessage(connection, message):
    message = fill_with_trash(message)
    sendWebMessage(message, connection)
    sendWebMessage("end", connection)

# Receives packages from the worker until it receive the (end) word
def recvWorkerMessage(connection):
    buffer = ""
    message = ""
    while True:
      message = connection.recv(PACKAGE_SIZE)
      message = message.decode("utf-8")
      message = message.replace('$','')
      if "end" in message:
        message = message.replace('end','')
        buffer += message
        break
      else:
        buffer += message
    return buffer

# @brief Gets ip of machine where script is running
def getIP():
    ip = 'NULL'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
      sock.connect(('8.8.8.8', 1))
      ip = sock.getsockname()[0]
    except Exception:
      pass
    sock.close()
    assert ip != 'NULL', "Could not get machine ip\n"
    return ip

def addHeaders(web_page):
    header = "HTTP/1.1 200 OK\n"
    header += "Content-Type: text/html\n\n"
    web_page = header+web_page
    return web_page

# Add 200 OK status and load html page 
# Return html loaded in a string
def loadHTML(web_page, name):
    html = ""
    file = open("web_resources/html/"+str(name)+".html", "r")
    for line in file:
      html += line
    return web_page+html

def loadCSS(web_page,name):
    css = "<style>"
    file = open("web_resources/css/"+str(name)+".css", "r")
    for line in file:
      css += line
    css += "</style>"
    web_page = web_page.replace("(CSS)", css)
    return web_page

def loadJS(web_page,name):
    js = "<script>"
    file = open("web_resources/js/"+str(name)+".js", "r")
    for line in file:
      js += line
    js += "</script>"
    web_page = web_page.replace("(JS)", js)
    return web_page

def loadWebPage(name, headers):
  web_page = ""
  if headers:
    web_page = addHeaders(web_page)
  web_page = loadHTML(web_page, name)
  web_page = loadCSS(web_page, "styles")
  web_page = loadJS(web_page, "draw_charts")
  return web_page