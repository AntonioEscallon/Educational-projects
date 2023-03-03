from socket import *
from datetime import datetime

# a villager exclusive function, 
def send_hunter(wolf_location):
     print("Sent hunter to {}!".format(wolf_location))


serverPort = 12002
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

counter = 0

print("Villager is listening...")
while counter < 3:
     connectionSocket, addr = serverSocket.accept()
     print("-> The shepherd boy is connected! Wake the hunter up. @ {}".format(datetime.now()))
     connectionSocket.settimeout(10)
     try:
          wolf_location = connectionSocket.recv(1024).decode()
          send_hunter(wolf_location) # a villager function
          connectionSocket.send("<- hunter sent".encode())
     except timeout:
          counter += 1
          print("We got tricked! counter: {} @ {}".format(counter, datetime.now()))
     connectionSocket.close()

serverSocket.close()
print("\"He cannot fool us again.\" the villagers said and stopped the TCP server.")