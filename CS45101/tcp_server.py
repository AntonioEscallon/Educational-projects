from socket import *
from datetime import datetime

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

knownID = []

print('The TCP server is ready to receive')
while True:
     connectionSocket, addr = serverSocket.accept()
     #print("--> server accepted a connection from {} @ {}".format(addr, datetime.now()))
     
     split = connectionSocket.recv(1024)
     sentence = split.split()
     new_id = sentence[1].decode()
     #print("--> server received {} @ {}".format(sentence, datetime.now()))
     
     if new_id in knownID:
          modifiedSent = "Nah " + str(new_id)
     else:
          knownID.append(new_id)
          modifiedSent = " OK " + new_id + " " + str(addr[0])+ " " + str(addr[1])
     
     #capitalizedSentence = sentence.upper()
     connectionSocket.send(modifiedSent.encode())
     #print("<- server sent {} @ {}".format(capitalizedSentence, datetime.now()))

     connectionSocket.close()

serverSocket.close()