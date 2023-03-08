from socket import *
import time
from datetime import datetime

#Setting all of the dtandards for the loopbacl
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(200)
knownID = {}

print("The UDP server is ready to receive")
while True:
    try: 
        split, clientAddress = serverSocket.recvfrom(1024) 
        #Splitting the message so that its easier to manipulate
        message = split.split()
        new_id = message[1].decode()

        if new_id in knownID.keys():
            #New conneciton is allowed after 30 seconds
            if(time.time() - (knownID[new_id])) > 30: 
                knownID[new_id] = time.time()
                modifiedMessage = "OK " + new_id + " " + str(clientAddress[0])+ " " + str(clientAddress[1])
            else:
                modifiedMessage = "RESET " + str(new_id)
        else:

            knownID[new_id] = time.time()
            modifiedMessage = "OK " + new_id + " " + str(clientAddress[0])+ " " + str(clientAddress[1])
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    except:
        serverSocket.close()
        print("Time Out")
        break
    else:
        continue