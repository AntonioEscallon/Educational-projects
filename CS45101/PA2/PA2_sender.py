#!/usr/bin/env python3
# Last updated: Jan, 2023
# Author: Phuthipong (Nikko)
import sys
import socket
import datetime
import time

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

def helperPacketSend(seq, bytes):
    text = bytes
    ACK = 0
    prefix = f"{seq} {seq} {text} "
    check = checksum(prefix)
    packet = prefix + str(check)
    return packet


def start_sender(connection_ID, loss_rate=0, corrupt_rate=0, max_delay=0, transmission_timeout=60):
    """
     This function runs the sender, connnect to the server, and send a file to the receiver.
     The function will print the checksum, number of packet sent/recv/corrupt recv/timeout at the end. 
     The checksum is expected to be the same as the checksum that the receiver prints at the end.

     Input: 
        connection_ID - String
        loss_rate - float (default is 0, the value should be between [0.0, 1.0])
        corrupt_rate - float (default is 0, the value should be between [0.0, 1.0])
        max_delay - int (default is 0, the value should be between [0, 5])
        tranmission_timeout - int (default is 60 seconds and cannot be 0)
     Output: None
    """

    ## STEP 0: PRINT YOUR NAME AND DATE TIME
    name = "Antonio Escallon"
    print("START receiver - {} @ {}".format(name, datetime.datetime.now()))

    ## STEP 1: CONNECT TO THE SERVER
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
        sys.exit()
    # disable timeout 
    clientSocket.settimeout(None)
    # request a relay service
    message = "HELLO S {} {} {} {}".format(loss_rate, corrupt_rate, max_delay, connection_ID)
    clientSocket.sendall(message.encode("utf-8"))
    print("sending: {}".format(message))
    # wait for message
    recv_message = clientSocket.recv(1024).decode("utf-8")
    print("received: {}".format(recv_message))
    # check response and keep waiting or terminate if the respond is not OK
    while not recv_message.startswith("OK"):
        if recv_message.startswith("WAITING"):
            # wait
            print("Waiting for a receiver")
            recv_message = clientSocket.recv(1024).decode("utf-8")
            
        elif recv_message.startswith("ERROR"):
            # print error and terminate
            print("Error: {}".format(recv_message.split(' ')[1]))
            exit()
        else:
            # invalid message, print and temrinate
            print("Error: Invalid message from server during connection. The message is {}".format(recv_message))
            exit()

    print("ESTABLISHED A CHANNEL @ {}".format(datetime.datetime.now()))

    ## STEP 2: READ FILE
    # read file
    filename = 'declaration.txt'
    with open(filename, 'r') as f:
        data = f.read()

    # some helpful variables but you don't have to use all of them
    pointer = 0
    SEQ = 0
    ACK = 0
    total_packet_sent = 0
    total_packet_recv = 0
    total_corrupted_pkt_recv = 0
    total_timeout =  0
    
    # set transmission timeout (set to 3 seconds if input is less or equal to zero)
    if transmission_timeout <= 0:
        transmission_timeout = 3
    clientSocket.settimeout(transmission_timeout)

    # send the first 200 characters
    to_send_size = 200

    # STEP 3: SEND FILE

    ##################################################
    # START YOUR RDT 3.0 SENDER IMPLEMENTATION BELOW #
    ##################################################
    sent_data = ""
    seq = 0
    expected = 0
    read = 0
    terminate = 0
    temp_data = ""
    #While loop to account for missing messages or time delays 
    while (terminate == 0):
        #Reading the first 200 bytes 
        while read < to_send_size:
            clientSocket.settimeout(transmission_timeout)
            read += 20 
            #Getting the first 20 bytes of every iteration of the while loop
            bytes = data[:20]
            temp_data += bytes
            #Moving the data 20 bytes further to account for the new message sent 
            data = data[20:]

            if data == ""  or len(data[:to_send_size]) == len(temp_data):
                #If we don't see any message we will add to the terminate number, which will cause the program to terminate after this cycle
                terminate = 1 
            
            #Helper method to create the packet. I was getting ovewhelmed with the amount of functions here so I decided to clean it up with the helper method. No real reason why it exists except for that. 
            packet = helperPacketSend(seq, bytes)
            sent_data += bytes
            #Creating an empty message function
            message = ""
            print(packet)
            while True:
                    clientSocket.send(packet.encode("utf-8"))
                    total_packet_sent +=1
                    try: 
                        #Decoding the recieved message 
                        message_recv = clientSocket.recv(1024).decode()
                    except:
                        #If we don't recieve a packet then we call a time out 
                        total_timeout += 1
                        continue
                    total_packet_recv += 1
                    #Check if we have the correct packet 
                    if checksum_verifier(message_recv):
                        #Check if seq numbers match. If they are then proceed to updated expected and seq numbers
                        if(int(message_recv[2]) == expected):
                            expected +=1
                            seq +=1
                            if(expected == 2):
                                expected = 0
                            if(seq == 2):
                                seq=0
                            break
                        else:
                            continue 
                    else:
                        #If wrong checksum then we have a corrupted package
                        #print("Wrong checksum")
                        total_corrupted_pkt_recv +=1
                        continue
            if (terminate == 1):
                data = sent_data
                break
        if(terminate == 1):
            data = sent_data
            break
        data = sent_data
    ########################################
    # END YOUR RDT 3.0 SENDER IMPLEMENTATION HERE #
    ########################################

    # close the socket
    clientSocket.close() 

    # print out your name, the date and time,
    print("DONE sender - {} @ {}".format(name, datetime.datetime.now()))

    # print checksum of the sent file 
    print("File checksum: {}".format(checksum(data[:to_send_size])))
    # print stats
    print("Total packet sent: {}".format(total_packet_sent))
    print("Total packet recv: {}".format(total_packet_recv))
    print("Total corrupted packet recv: {}".format(total_corrupted_pkt_recv))
    print("Total timeout: {}".format(total_timeout))
 
if __name__ == '__main__':
    # check arguments
    if len(sys.argv) != 6:
        print("Expected \"python PA2_sender.py <connection_id> <loss_rate> <corrupt_rate> <max_delay> <transmission_timeout>\"")
        exit()
    connection_ID, loss_rate, corrupt_rate, max_delay, transmission_timeout = sys.argv[1:]
    # start sender
    start_sender(connection_ID, loss_rate, corrupt_rate, max_delay, float(transmission_timeout))
