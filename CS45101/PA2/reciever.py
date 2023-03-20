#!/usr/bin/env python3
# Last updated: Jan, 2023
# Author: Phuthipong (Nikko)
import sys
import time
import socket
import datetime 

CONNECTION_TIMEOUT = 60

# for testing with gaia server
SERVER_IP = "128.119.245.12"
SERVER_PORT = 20008

def checksum(msg):
    """
     This function calculates checksum of an input string
     Note that this checksum is not Internet checksum.
    
     Input: msg - String
     Output: String with length of five
     Example Input: "1 0 That was the time fo "
     Expected Output: "02018"
    """

    # step1: covert msg (string) to bytes
    msg = msg.encode("utf-8")
    s = 0
    # step2: sum all bytes
    for i in range(0, len(msg), 1):
        s += msg[i]
    # step3: return the checksum string with fixed length of five 
    #        (zero-padding in front if needed)
    return format(s, '05d')

def checksum_verifier(msg):
    """
     This function compares packet checksum with expected checksum
    
     Input: msg - String
     Output: Boolean - True if they are the same, Otherwise False.
     Example Input: "1 0 That was the time fo 02018"
     Expected Output: True
    """

    expected_packet_length = 30
    # step 1: make sure the checksum range is 30
    if len(msg) < expected_packet_length:
        return False
    # step 2: calculate the packet checksum
    content = msg[:-5]
    calc_checksum = checksum(content)
    expected_checksum = msg[-5:]
    # step 3: compare with expected checksum
    if calc_checksum == expected_checksum:
        return True
    return False

def start_receiver(connection_ID, loss_rate=0.0, corrupt_rate=0.0, max_delay=0.0):
    """
     This function runs the receiver, connnect to the server, and receiver file from the sender.
     The function will print the checksum of the received file at the end. 
     The file checksum is expected to be the same as the checksum that the sender prints at the end.

     Input: 
        connection_ID - String
        loss_rate - float (default is 0, the value should be between [0.0, 1.0])
        corrupt_rate - float (default is 0, the value should be between [0.0, 1.0])
        max_delay - int (default is 0, the value should be between [0, 5])
     Output: None
    """

    ## STEP 0: PRINT YOUR NAME AND DATE TIME
    name = "Anotnio Escallon"
    print("START receiver - {} @ {}".format(name, datetime.datetime.now()))

    ## STEP 1: connect to the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set connection timeout
    clientSocket.settimeout(CONNECTION_TIMEOUT)
    try:
        # connect to the server
        clientSocket.connect((SERVER_IP,SERVER_PORT))
    except socket.error as e:
        # print error and terminate if fail
        print('Connection error: {}'.format(e))
        clientSocket.close()
        return
    # disable timeout 
    clientSocket.settimeout(None)
    # request a relay service
    message = "HELLO R {} {} {} {}".format(loss_rate, corrupt_rate, max_delay, connection_ID)
    clientSocket.sendall(message.encode("utf-8"))
    # wait for message
    recv_message = clientSocket.recv(1024).decode("utf-8")
    print("received: {}".format(recv_message))
    # check response and keep waiting or terminate if the respond is not OK
    while not recv_message.startswith("OK"):
        if recv_message.startswith("WAITING"):
            # wait
            print("Waiting for a sender")
            recv_message = clientSocket.recv(1024).decode("utf-8")
            
        elif recv_message.startswith("ERROR"):
            # print error and terminate
            print("Error: {}".format(recv_message[6:]))
            # exit()
            return
        else:
            # invalid message, print and temrinate
            print("Error: Invalid message format from server during connection phrase... {}".format(recv_message))
            # exit()
            return

    print("ESTABLISHED A CHANNEL @ {}".format(datetime.datetime.now()))

    # STEP 2: receive file
    
    data = ""
    total_packet_sent = 0
    total_packet_recv = 0
    total_corrupted_pkt_recv = 0

    ####################################################
    # START YOUR RDT 3.0 RECEIVER IMPLEMENTATION BELOW #
    ####################################################
    expected = 0
    check = True
    if check:
        while True: 
            message = clientSocket.recv(1024).decode()
            if not message:
                break
            num = message[0]
            ack = num
            if checksum_verifier(message) and num == str(expected):
                data += message[4:-6]
                expected = 1-expected
            else:
                ack = 1 - expected
        prefix = f' {ack}  '
        message_checksum = checksum(prefix)
        packet = f' {ack}   {message_checksum}'
        clientSocket.send(packet.encode())

    #################################################
    # END YOUR RDT 3.0 RECEIVER IMPLEMENTATION HERE #
    #################################################

    # close the socket
    clientSocket.close() 

    # remove space at the end
    data = data.rstrip(' ')
    # print(data)

    # print out your name, the date and time,
    print("DONE receiver - {} @ {}".format(name, datetime.datetime.now()))

    # print checksum of the received file 
    print("File checksum: {}".format(checksum(data)))
    # print stats
    print("Total packet sent: {}".format(total_packet_sent))
    print("Total packet recv: {}".format(total_packet_recv))
    print("Total corrupted packet recv: {}".format(total_corrupted_pkt_recv))
    # reminder: no timeout on receiver

    # write received data into a file
    # with open('download.txt', 'w') as f:
    #     f.write(data)
 
if __name__ == '__main__':
    # check arguments
    if len(sys.argv) != 5:
        print("Expected \"python PA2_receiver.py <connection_id> <loss_rate> <corrupt_rate> <max_delay>\"")
        exit()

    # assign arguments
    connection_ID, loss_rate, corrupt_rate, max_delay = sys.argv[1:]

    # START RECEIVER
    start_receiver(connection_ID, loss_rate, corrupt_rate, max_delay)