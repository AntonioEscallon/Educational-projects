from socket import *
import time

serverName = '127.0.0.1'
serverPort = 12002

while True:
	wolf_location = input('See a wolf? Report the location:')

	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName,serverPort))

	clientSocket.send(wolf_location.encode())
	villager_response = clientSocket.recv(1024)
	print ('Villager said:', villager_response.decode())
	
	clientSocket.close()
	time.sleep(3)
