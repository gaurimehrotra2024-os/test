import subprocess
import sys

program = sys.argv[1]
username = sys.argv[2]

passwords = [
    '1',
    '12',
    '123',
    '1234',
    '12345',
    '123456',
    '12345678',
    '123123123',
]

for password in passwords:
    try:
        result = subprocess.run([program, username, password], stdout=subprocess.DEVNULL, shell=False, check=True)
        print("cracked! user: {} password: {}".format(username, password))
        break
    except subprocess.CalledProcessError:
        continue