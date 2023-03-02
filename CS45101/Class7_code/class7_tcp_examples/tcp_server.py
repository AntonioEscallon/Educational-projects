from socket import *
from datetime import datetime

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The TCP server is ready to receive')
while True:
     connectionSocket, addr = serverSocket.accept()
     print("--> server accepted a connection from {} @ {}".format(addr, datetime.now()))
     
     sentence = connectionSocket.recv(1024).decode()
     print("--> server received {} @ {}".format(sentence, datetime.now()))
     
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence.encode())
     print("<- server sent {} @ {}".format(capitalizedSentence, datetime.now()))

     connectionSocket.close()

serverSocket.close()