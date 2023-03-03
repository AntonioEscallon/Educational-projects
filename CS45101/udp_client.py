from socket import *
from datetime import datetime

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence: ')
split = message.split()

word = split[0]
id = split[1]

newmess = word + " " + id

clientSocket.sendto(newmess.encode(), (serverName, serverPort))
#print("<- client sent {} to {} @ {}".format(message, (serverName, serverPort), datetime.now()))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
recievedMess = modifiedMessage.decode()

if recievedMess.split()[0] == "OK":
    print("Nice " + recievedMess[3:])
if recievedMess.split()[0] == "Nah":
    print("Connection Error" + recievedMess.split()[1])
    id = input("New Connection ID: ")
    newmess = word + " " + id
    clientSocket.sendto(newmess.encode(), (serverName, serverPort))



#print("--> client received {} from {} @ {}".format(modifiedMessage.decode(), serverAddress, datetime.now()))

#print(modifiedMessage.decode())

clientSocket.close()
print("Done!")
