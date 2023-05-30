from socket import *
import time
from datetime import datetime

message = input('Input lowercase sentence: ')
split = message.split()


serverName = split[1]
serverPort = int(split[2])

clientSocket = socket(AF_INET, SOCK_DGRAM)

word = split[0]
id = split[3]

newmess = word + " " + id

clientSocket.settimeout(60)

clientSocket.sendto(newmess.encode(), (serverName, serverPort))
#print("<- client sent {} to {} @ {}".format(message, (serverName, serverPort), datetime.now()))
count = 0
try: 
    while count <4:
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        recievedMess = modifiedMessage.decode()
        recievedSplit = recievedMess.split()
        
        if recievedSplit[0] == "OK":
            print("OK " + recievedMess[3:] + " on ",  datetime.now())
            break
        if recievedSplit[0] == "RESET":
            if count == 2: 
                print("Conneciton Failure on", datetime.now())
                break
            print("Connection Error " + recievedSplit[1] + " on ",  datetime.now())
            print("RESET " + recievedSplit[1])
            id = input("New Connection ID: ")
            newmess = word + " " + id
            clientSocket.sendto(newmess.encode(), (serverName, serverPort))
        count+=1
except:
    print("Time Out")

clientSocket.close()
