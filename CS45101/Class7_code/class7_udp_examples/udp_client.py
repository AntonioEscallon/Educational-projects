from socket import *
from datetime import datetime

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence: ')

clientSocket.sendto(message.encode(), (serverName, serverPort))
print("<- client sent {} to {} @ {}".format(message, (serverName, serverPort), datetime.now()))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print("--> client received {} from {} @ {}".format(modifiedMessage.decode(), serverAddress, datetime.now()))

print(modifiedMessage.decode())

clientSocket.close()
print("Done!")
