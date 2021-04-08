import sys 
import socket 
import select

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if len(sys.argv) != 3 :
    print("it should be used like : chat_server.py <ip> <port>")
    exit()


#getting the ip and port
IP_addr = str(sys.argv[1])
Port = int(sys.argv[2])

#bind the sever to the given ip and port 
server.connect((IP_addr,Port))

while True:
    sockets_list = [sys.stdin,server]

    #no timeout in select to block untill a change is made in the lists

    r_socket, wr_socket, err_socket = select.select(sockets_list,[],[])

    for scks in r_socket:
        if scks == server : 
            # this means that the chat server is sending to us (the client)
            message = scks.recv(4096)
            message_ = '<'+'received'+'>'+str(message)
            #TODO maybe more sofisticated log message  ?? 
            print(message_)

        else: 
            #in this case the read op is from the terminal 
            # we read from it and send to the server 
            message = sys.stdin.readline()
            server.send(b'message')
            print('<you>'+message)
            sys.stdout.flush()

server.close()

