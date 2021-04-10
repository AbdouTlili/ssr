from crypto import MyCrypto

c = MyCrypto("abdou_test")

c._create_dir()
c._create_passwd_file()
c.create_private_key()
c.create_public_key()