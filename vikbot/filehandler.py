import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

password_provided = "asdw"  
password = password_provided.encode()  
salt = b'\x81t\xd4C+\x92\x82O\xd0\x18du\xb6}\xcd\x7f'

def decode(msg):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    decoded = f.decrypt(msg.encode())
    return decoded.decode()

def encode(msg):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    encoded = f.encrypt(msg.encode())
    return encoded.decode()

def readsettings(segment):
    with open("/home/ubuntu/bots/vikbot/settings/settings.json", "r") as fp:
        tmpdict = json.loads(fp.read())

    for dicts in tmpdict :  
        if(dicts["name"] == segment):
            tmpdict = dicts

    data = tmpdict["data"]
    if tmpdict["encryption"] == 1 :
        data = decode(msg=tmpdict["data"])

    return data


def updatesettings(segment, data):

    with open("/home/ubuntu/bots/vikbot/settings/settings.json", "r") as fp:
        tmpdict = json.loads(fp.read())
    
    for dicts in tmpdict:
        if dicts["name"] == segment:
            if dicts["encryption"] == 1:
                dicts["data"] = encode(data)
            else:
                dicts["data"] = data

    print(tmpdict)

    with open("/home/ubuntu/bots/vikbot/settings/settings.json", "w") as fp:
        json.dump(tmpdict, fp)
