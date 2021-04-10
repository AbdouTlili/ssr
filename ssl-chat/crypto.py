import subprocess 
import os 
import socket
import string
import secrets
import time

class MyCrypto:

    def __init__(self,user_id):
        self.user_id = user_id
        self.path = "./"+user_id
        self._create_dir()
        self._create_passwd_file()
        self.create_private_key()
        self.create_public_key()

    def _get_public_key(self):
        public_key = open(f"{self.path}/src_rsa_pub.pem", 'r').read()
        return public_key

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
        cmd = "openssl genrsa -out "+self.path+"/src_rsa.pem -passout pass:"+self.path+"/srcpasswd -des 512"
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
        cmd = "openssl rsa -in "+self.path+"/src_rsa.pem -passin pass:"+self.path+"/srcpasswd -out "+self.path+"/src_rsa_pub.pem -pubout"
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
        server.settimeout(2.0) # configure a timeout value of 3 seconds
        while True:
            try:
                response = server.recv(4096)   # get the packet received (if any)
                
                if response.decode() == "start handshake":
                    pkey = self._get_public_key()
                    server.send("handshake".encode())
                    server.send(pkey.encode())
                    print(f"public key of {self.user_id} sent to peer")

                elif response.decode() == "handshake":
                    response = server.recv(4096)
                    self._save_peer_pkey(response.decode())
                    print("peers public key received ")
                    return 0 
                
            except socket.timeout:
                print('No handshake request received ')

                try:
                    server.send("start handshake".encode())
                except: 
                    pass



