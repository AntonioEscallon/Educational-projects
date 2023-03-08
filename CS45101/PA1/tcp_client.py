from socket import *
from datetime import datetime
import time

#try: 
    
sentence = input('Input lowercase sentence: ')
#Splitting all of the sentences in their correct location
split = sentence.split()
word = split[0]
id = split[1]
serverName = split[1]
serverPort = int(split[2])
clientSocket = socket(AF_INET, SOCK_STREAM)
print("client and server are now connected @ {}".format(datetime.now()))

newsent = word + " " + id

try: 
    #Connecting to the server with the given input
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(newsent.encode())
    clientSocket.settimeout(15)

    count = 0
    try: 
        while count < 4: 
            modifiedSentence = clientSocket.recv(1024)
            decodedSent = modifiedSentence.decode()
            #Splitting the message to identify the first part and go into the if statmenets depending on that
            decodedSplit = decodedSent.split()
            if decodedSplit[0] == "OK":
                print("Connection established " + decodedSent[3:] + " on", datetime.now())
                break
            if decodedSplit[0] == "RESET":
                #Making sure we print that there was an error
                print("Connection Error " + decodedSplit[1] + " on", datetime.now())
                if count == 2: 
                    print("Connection Failure" + " on", datetime.now())
                    break
                id = input("New Connection ID required: ")
                newsent = word + " " + id
                #I was delaing with a broken pipe error becuase the connection was being temrinated.
                #Seemed like the easiest thing to do was re-establish the connection, which is why I 
                #added the code chunk below. 
                clientSocket.close()
                clientSocket = socket(AF_INET, SOCK_STREAM) 
                clientSocket.connect ((serverName,serverPort))
                #Then we just send the message again
                clientSocket.send(newsent.encode())
            count +=1
    except: 
        print("Time Out!")
except:
    print("Conneciton Failure")

clientSocket.close()