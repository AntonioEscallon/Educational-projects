from socket import *
import time

serverName = '127.0.0.1'
serverPort = 12002

while True:
	try:
		_ = input('Ready to trick the villagers? (press enter to continue):')
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect((serverName,serverPort))
		print('Socket connected! Let\'s take a 12-seconds nap.')
		time.sleep(12)
		print("Successfully tricked them!")
		
	except ConnectionRefusedError:
		print("Villagers don't listen to me anymore!")
		exit()
