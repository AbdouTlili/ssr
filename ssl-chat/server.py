import socket 
import sys
from _thread import *

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#checking if add three args are provided 
if len(sys.argv) != 3 :
    print("it should be used like : chat_server.py <ip> <port>")
    exit()

#getting the ip and port
IP_addr = str(sys.argv[1])
Port = int(sys.argv[2])

#bind the sever to the given ip and port 
server.bind((IP_addr,Port))

server.listen(20)

list_of_clients = []

def client_thread(conn,addr):
    
    # hello message to the client with conn object 

    conn.send(b"successfuly connected to ssl-chat server !!")

    while True : 
        try:
            message = conn.recv(4096)

            if message : 

                #NOTE i dont know yet if the log here will be needed later on
                message_ = '<'+addr[0]+'>'+message
                # print the logs in the servers terminal 
                print(message_)
                
                send(message_, conn)

            else : 
                #FIXME when the message has no content 
                remove(conn)

        except : 
            continue 


def send(message,connection): 
    for client in list_of_clients:
        if client != connection :
            try:
                client.send(b'message')

            except :
                client.close()

                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

print('server started.. \nwaiting for connections..')
while True : 

    #accept connection requests and return two oarams needed :
    # 'conn' which is a socket object  
    # and 'addr' which is the address of the client 
    conn, addr = server.accept()

    list_of_clients.append(conn)

    #TODO the connection log is printed to the server's terminal 
    connection_log_msg = '<'+'log'+'>'+' user :'+str(addr)+' just connected'
    print('\n'+connection_log_msg)

    #creating a thread for every user 
    start_new_thread(client_thread,(conn,addr))

conn.close()
server.close()