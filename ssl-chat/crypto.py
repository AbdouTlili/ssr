import subprocess 
import os 
import socket
import string
import secrets
import re
import time

class MyCrypto:

    def __init__(self,user_id):
        self.user_id = user_id
        self.path = "./."+user_id
        self._create_dir()
        self._create_passwd_file()
        self.create_private_key()
        self.create_public_key()

    def _get_public_key(self):
        public_key = open(f"{self.path}/src_rsa_pub.pem", 'r').read()
        return public_key

    def _extract_message(self, message):
        """
            This function will just extract the message received from data received
            because data is received in this form from the server  <ip_add>+message
        """
        found = re.sub(r'<[0-9]+.[0-9]+.[0-9]+.[0-9]+>','', message)
        return found
        
    def _save_peer_pkey(self,pkey):
        open(f"{self.path}/dest_rsa_pub.pem", 'w').write(pkey)



    def _create_dir(self):
        # create a dir for the use to store its keys and files 
        try :
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            else: 
                pass
        except OSError:
            print("error while creating a dir for the use in " + self.path)
            exit(-1)
        else :
            print("dir " + self.path + " created for user")

    def _create_passwd_file(self):

        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(128))
        try : 
            with open(self.path+"/srcpasswd","w") as f :
                f.write(password)
                f.close()
        except : 
            print(f"error while creating the passwd file for {self.user_id}")


    def create_private_key(self):
        password = open(f"{self.path}/srcpasswd", "r").read()
        cmd = f"openssl genrsa -out {self.path}/src_rsa.pem -passout pass:{password} -des 512"
        try : 
            res = subprocess.run(cmd.split(),\
                stdout=subprocess.PIPE,\
                stderr=subprocess.PIPE)
                # print(res.stderr)
        except : 
            print("error executing \"openssl genrsa\" command ")

        if "Generating RSA private key" in str(res.stderr): 
            print(f"-> private key created successfullyfor {self.user_id} ")
        else : 
            print(f"-> an error occured wihle generating the Private key of {self.user_id}")



    def create_public_key(self):
        password = open(f"{self.path}/srcpasswd", "r").read()
        cmd = f"openssl rsa -in {self.path}/src_rsa.pem -passin pass:{password} -out {self.path}/src_rsa_pub.pem -pubout"
        try : 
            res = subprocess.run(cmd.split(),\
                stdout=subprocess.PIPE,\
                stderr=subprocess.PIPE)
                # print(res.stderr)
        except : 
            print("error executing \"openssl genrsa\" command ")
        if "writing RSA key" in str(res.stderr): 
            print(f"-> Public key created successfullyfor {self.user_id} ")
        else : 
            print(f"-> an error occured wihle generating the Public key of {self.user_id}")

    def handshake(self,server):
        # this will allow us to stop sending non sense "start handshake" messages after we have started the handshake
        INITIATED_HANDSHAKE = False
        server.settimeout(2.0) # configure a timeout value of 3 seconds
        while True:
            try:
                response = server.recv(4096)   # get the packet received (if any)
                # this is the signal to initiate the handshake 
                if  self._extract_message(response.decode()) == "start handshake":
                    pkey = self._get_public_key()
                    # here send also the shared key 
                    server.send("handshake".encode())
                    server.send(pkey.encode())
                    print(f"public key of {self.user_id} sent to peer")
                    INITIATED_HANDSHAKE = True
                # this is the signale to receive the public key and send the client pubkey 
                elif self._extract_message(response.decode()) =="handshake":
                    response = server.recv(4096)
                    self._save_peer_pkey(self._extract_message(response.decode()))
                    print("peers public key received ")
                    pkey = self._get_public_key()
                    # here send also the shared key 
                    server.send("handshake-response".encode())
                    server.send(pkey.encode())
                    INITIATED_HANDSHAKE = True
                # this is the signal to receive the second pubkey and start creating the shared key 
                elif self._extract_message(response.decode()) =="handshake-response":
                    response = server.recv(4096)
                    self._save_peer_pkey(self._extract_message(response.decode()))
                    print("peers public key received ")
                
            except socket.timeout:
                print('No handshake request received ')
                if not INITIATED_HANDSHAKE:
                    try:
                        server.send("start handshake".encode())
                    except: 
                        pass



