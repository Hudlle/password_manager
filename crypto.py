from cryptography.fernet import Fernet

def generateKey():
    key = Fernet.generate_key()
    
    with open("key.key", "wb") as keyFile:
        keyFile.write(key)

def loadKey():
    return open("key.key", "rb").read()

key = loadKey()
f = Fernet(key)
def encryptMessage(m):
    m = m.encode()
    m = f.encrypt(m)
    return m

def decryptMessage(m):
    m = m.encode()
    m = f.decrypt(m).decode()
    return m