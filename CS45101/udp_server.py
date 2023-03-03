from socket import *
from datetime import datetime

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

knownID = []

print("The UDP server is ready to receive")
while True:
    split, clientAddress = serverSocket.recvfrom(2048) # if the buf size value is smaller than the datagram size, it will drop the rest.
    message = split.split()
    new_id = message[1].decode()

    if new_id in knownID:
        modifiedMessage = "Nah " + str(new_id)
    #print("--> server received {} from {} @ {}".format(message.decode(), clientAddress, datetime.now()))
    else:
        knownID.append(new_id)
        modifiedMessage = " OK " + new_id + " " + str(clientAddress[0])+ " " + str(clientAddress[1])
    #modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    print("<- server sent {} to {} @ {}".format(modifiedMessage, clientAddress, datetime.now()))

