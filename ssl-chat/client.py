import sys 
import socket 
import select
import os
from crypto  import MyCrypto
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if len(sys.argv) != 4 :
    print("it should be used like : chat_server.py <ip> <port> <client_id> ")
    exit()


#getting the ip and port
IP_addr = str(sys.argv[1])
Port = int(sys.argv[2])
client_id = str(sys.argv[3])

# create a directory where to store keys and received messages !!
crypto = MyCrypto(client_id)


#bind the sever to the given ip and port 
server.connect((IP_addr,Port))

## TODO  update the handshale function


crypto.handshake(server)


#while True: 
#  
#    # maintains a list of possible input streams 
#    sockets_list = [sys.stdin, server] 
#  
#    """ There are two possible input situations. Either the 
#    user wants to give manual input to send to other people, 
#    or the server is sending a message to be printed on the 
#    screen. Select returns from sockets_list, the stream that 
#    is reader for input. So for example, if the server wants 
#    to send a message, then the if condition will hold true 
#    below.If the user wants to send a message, the else 
#    condition will evaluate as true"""
#    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
#
#  
#    for socks in read_sockets: 
#        if socks == server: 
#            message = socks.recv(4096) 
#            ## decrypt and verify signature  
#            ## using sharedkey variable 
#            message = message.decode()
#            print(message) 
#            sys.stdout.flush() 
#        else: 
#            message = sys.stdin.readline() 
#            ## encrypt and sign 
#            ## using sharedkey variable 
#            message_as_byte = message.encode()
#            server.send(message_as_byte) 
#            print("<You>"+message) 
#            sys.stdout.flush() 
server.close() 