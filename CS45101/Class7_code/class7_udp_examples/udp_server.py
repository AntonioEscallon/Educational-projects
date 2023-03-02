from socket import *
from datetime import datetime

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("The UDP server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048) # if the buf size value is smaller than the datagram size, it will drop the rest.
    print("--> server received {} from {} @ {}".format(message.decode(), clientAddress, datetime.now()))
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    print("<- server sent {} to {} @ {}".format(modifiedMessage, clientAddress, datetime.now()))

