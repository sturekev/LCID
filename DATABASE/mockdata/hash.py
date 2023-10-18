# REMEMBER TO UPDATE Authenticate/hash.py when you update this file


import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

## Password verify
# encode 
def encodePassword (password:str): 
    return password.encode('utf-8')

# run before save it in db 
def hashedPassword (endcodePassword):
    return bcrypt.hashpw(endcodePassword, bcrypt.gensalt())

# verify
def checkPassword (endcodePassword, hashed: bytes):
    if bcrypt.checkpw(endcodePassword, hashed):
        return True
    return False
## 

## RSAGenKey
def RsaGenKey(bits=2048):
    return RSA.generate(bits)

# RSA sign the message
def generateSignature(message: str, priKey):
    byteMsg = message.encode('utf-8')
    h = SHA256.new(byteMsg)
    return pkcs1_15.new(RSA.import_key(priKey)).sign(h)

def verifyKey (message: str,signature: bytes,pubKey: bytes) -> bool:
    h = SHA256.new(message)
    try:
        pkcs1_15.new(pubKey).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
# return Byte 
def ExportNewRSAKey() -> bytes:
    keyPair = RsaGenKey()
    PubKey = keyPair.publickey().export_key()  # Export public key
    PriKey = keyPair.export_key()  # Export private key
    return PubKey, PriKey

# return Byte
def EncryptPubKey(pubKey: bytes, message: str) -> bytes: 
    byteMsg = message.encode('utf-8')
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(pubKey))
    ciphertext = cipher_rsa.encrypt(byteMsg)
    return ciphertext

#r return String  
def DecryptPriKey (private_key: bytes, message: str):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    message = cipher_rsa.decrypt(message)
    return message.decode('utf-8')

def extractRSAkey (key: str):
    return key[:258],key[258:]

def genKeytoStr (key: bytes):
    return hex(key)

def genStrtoBytes (key: str):
    pass
##

