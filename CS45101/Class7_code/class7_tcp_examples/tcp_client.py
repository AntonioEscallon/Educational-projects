from socket import *
from datetime import datetime

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print("client and server are now connected @ {}".format(datetime.now()))

sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode())
print("<- client sent {} to the server @ {}".format(sentence, datetime.now()))

modifiedSentence = clientSocket.recv(1024)
# print ('From Server:', modifiedSentence.decode())
print("--> client received {} from the server @ {}".format(modifiedSentence.decode(), datetime.now()))

clientSocket.close()
