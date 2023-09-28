from Crypto.PublicKey import RSA
from hashlib import sha512

def RsaGenKey():
    keyPair = RSA.generate(bits=1024)
    # return keyPair.n, keyPair.e, keyPair.d
    return keyPair 

# RSA sign the message
def generateSignature(message: bytes, keyPair_d, keyPair_n):
    hash = int.from_bytes(sha512(message).digest(), byteorder='big')
    return pow(hash, keyPair_d, keyPair_n)
def verifykey (msg,signature,keyPair_e, keyPair_n):
    hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
    hashFromSignature = pow(signature, keyPair_e, keyPair_n)
    return hash == hashFromSignature

def encodeRSAKey ():
    pass
keyPair = RSA.generate(bits=1024)
n=hex(keyPair.n)
e=hex(keyPair.e)
d=hex(keyPair.d)
print (len(e))
print (len(n))
print (len(d))

# RSA sign the message
msg = b'A message for signing'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
signature = pow(hash, keyPair.d, keyPair.n)
print (signature)
print (type(signature))
# RSA verify signature
msg = b'A message for signing'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
hashFromSignature = pow(signature, keyPair.e, keyPair.n)
print (hashFromSignature)
print(type(hashFromSignature))
print("Signature valid:", hash == hashFromSignature)