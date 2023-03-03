import socket
from socket import client_thread 

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind((socket.gethostname(), 80))
serversock.listen(5)

while True:
    # accept connections from outside
    (clientsocket, address) = serversock.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()