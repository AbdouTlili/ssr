## TODO implement  encrypt , decrypt and sign and verify signature 




openssl genrsa -out src_rsa.pem -passout pass:srcpasswd -des 512
openssl rsa -in src_rsa.pem -passin pass:srcpasswd -out src_rsa_pub.pem -pubout


#assymetric 
Chiffrer un secret avec la clé publique du destinataire : 
openssl rsautl -in secret.txt -out secret.crypt -inkey dest_rsa_pub.pem -pubin -encrypt

Déchiffrement d'un secret avec la clé privée du destinataire : 
openssl rsautl -decrypt -in secret.crypt -out secret.txt -inkey dest_rsa.pem



########33 symetric : 

Chiffrement d un message avec un secret (clé symétrique) en utilisant
l algorithme DES-CBC:
 openssl enc -des-cbc -in message.txt -out message.crypt -pass file:secret.txt

Déchiffrement du "message.crypt" à l'aide de secret qui se trouve dans
"secret.txt" : 
openssl enc -in message.crypt -out messagee.txt -pass file:secret.txt -d -des-cbc


# calcul de hash 

Calcul de condensat (code de hashage) avec MD5 : 
openssl dgst -md5 -binary -out message.crypt.dgst message.crypt

#calcul de signature 

 Chiffrement du condensat (code de hashage) avec la clé privée de la
source "src_rsa.pem" : 
openssl rsautl -in message.crypt.dgst -out message.crypt.dgst.sign -sign -inkey src_rsa.pem

 Déchiffrement de l'empreinte (code de hashage) du message vers dgst1 :
openssl rsautl -in message.crypt.dgst.sign -out dgst1 -pubin
-inkey src_rsa_pub.pem

