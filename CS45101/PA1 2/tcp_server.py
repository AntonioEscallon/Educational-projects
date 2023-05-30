from socket import *
from datetime import datetime
import time 

#Setting all of the standards for the loopback
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

knownID = {}
serverSocket.settimeout(120)
print('The TCP server is ready to receive')
while True:
    try: 
        connectionSocket, addr = serverSocket.accept()
        #print("--> server accepted a connection from {} @ {}".format(addr, datetime.now()))
        
        #Splitting the message so that its easier to manipulate
        split = connectionSocket.recv(1024)
        sentence = split.split()
        new_id = sentence[1].decode()
       
        if new_id in knownID.keys():
            #After 30 seconds we can use the same connection ID
            if(time.time() - knownID[new_id])>= 30:
                knownID[new_id] = time.time()
                modifiedSent = "OK " + new_id + " " + str(addr[0])+ " " + str(addr[1])
            else:
                modifiedSent = "RESET " + str(new_id)
        else:
            knownID[new_id] = time.time()
            modifiedSent = "OK " + new_id + " " + str(addr[0])+ " " + str(addr[1])
        
        #capitalizedSentence = sentence.upper()
        connectionSocket.send(modifiedSent.encode())
        #print("<- server sent {} @ {}".format(capitalizedSentence, datetime.now()))
        connectionSocket.close()

    except:
        connectionSocket.close()
        print("Time Out!")
        break
    else:
        continue
serverSocket.close()