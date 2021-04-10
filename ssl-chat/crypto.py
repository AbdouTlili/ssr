import subprocess 
import os 
import uuid 

class MyCrypto:

    def __init__(self,user_id):
        self.user_id = user_id
        self.path = "./"+user_id

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
        try : 
            with open(self.path+"/srcpasswd","w") as f :
                f.write(str(uuid.uuid1()))
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

