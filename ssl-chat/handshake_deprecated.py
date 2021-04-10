### TODO Implement handshake functions !!!
import os 


import secrets
import string

def handshake(server, generate,password):
    ## generate public+ private key 
    result = os.system(f'openssl genrsa -out priv.pem -passout pass:{password} -des 1024')
    if result != 0 :
        print("An error just happened in the priv keygeneration")
    result = os.system(f"openssl rsa -in priv.pem -passin pass:{password} -out pub.pem -pubout")
    if result != 0 :
        print("An error just happened in the pub key generation")
    # send public key 
    public_key = open("pub.pem", 'r').read()
    server.send(public_key.encode('utf-8'))
    # receive public key from other client 
    pubkey = server.recv(1024)
    print(pubkey)
    if generate:
        print("Generating the secret shared key !! ") 
        alphabet = string.ascii_letters + string.digits
        secret_key = ''.join(secrets.choice(alphabet) for i in range(20))
        open("key_shared.txt", 'w').write(secret_key)
        print("Shared Key generated successfully")








