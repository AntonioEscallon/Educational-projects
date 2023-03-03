from socket import *
from datetime import datetime

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print("client and server are now connected @ {}".format(datetime.now()))

sentence = input('Input lowercase sentence: ')
split = sentence.split()

word = split[0]
id = split[1]

newsent = word + " " + id
clientSocket.send(newsent.encode())
#print("<- client sent {} to the server @ {}".format(sentence, datetime.now()))

modifiedSentence = clientSocket.recv(1024)
decodedSent = modifiedSentence.decode()

decodedSplit = decodedSent.split()
#print(decodedSplit)
if decodedSplit[0] == " OK ":
    print("Les go " + decodedSent[3:])
if decodedSplit[0] == "Nah":
    print("Connection Error " + decodedSplit[1])
    id = input("New Connection ID: ")
    newsent = word + " " + id
    clientSocket.sendto(newsent.encode(), (serverName, serverPort))

# print ('From Server:', modifiedSentence.decode())
print("--> client received {} from the server @ {}".format(modifiedSentence.decode(), datetime.now()))

clientSocket.close()
