# import bcrypt
# from Crypto.PublicKey import RSA
# from hashlib import sha512

# ## Password verify
# def encodePassword (password:str): 
#     return password.encode('utf-8')

# def hashedPassword (endcodePassword):
#     return bcrypt.hashpw(endcodePassword, bcrypt.gensalt())

# def checkPassword (endcodePassword, hashed: bytes):
#     if bcrypt.checkpw(endcodePassword, hashed):
#         return True
#     return False
# ## 

# ## RSAGenKey
# def RsaGenKey():
#     keyPair = RSA.generate(bits=1024)
#     # return keyPair.n, keyPair.e, keyPair.d
#     return keyPair 

# # RSA sign the message
# def generateSignature(message: bytes, keyPair_d, keyPair_n):
#     hash = int.from_bytes(sha512(message).digest(), byteorder='big')
#     return pow(hash, keyPair_d, keyPair_n)
# def verifykey (msg,signature,keyPair_e, keyPair_n):
#     hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
#     hashFromSignature = pow(signature, keyPair_e, keyPair_n)
#     return hash == hashFromSignature

# def encodeRSAKey ():
#     keyPair = RsaGenKey()
#     PubKey = hex(keyPair.n) + hex(keyPair.e)
#     Prikey = hex(keyPair.n) + hex(keyPair.d)
#     return PubKey, Prikey

# def extractRSAkey (key):
#     return key[:258],key[258:]
# ##

