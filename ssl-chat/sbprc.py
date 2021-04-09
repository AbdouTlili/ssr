import subprocess

useless_cat_call = subprocess.run(["openssl","help"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(useless_cat_call.stderr)  # Hello from the other side