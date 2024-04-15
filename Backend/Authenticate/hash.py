# REMEMBER TO UPDATE mockdata/hash.py when you update this file

import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

## Password verify
# encode 
def encode_password (password:str): 
    return password.encode('utf-8')

# run before save it in db 
def hashed_password (encode_password):
    return bcrypt.hashpw(encode_password, bcrypt.gensalt())

# verify
def check_password (encode_password, hashed: bytes):
    if bcrypt.checkpw(encode_password, hashed):
        return True
    return False
## 

## rsa_key_generator
def rsa_key_generator(bits=2048):
    return RSA.generate(bits)

# RSA sign the message
def generate_signature(message: str, public_key):
    byte_msg = message.encode('utf-8')
    hash = SHA256.new(byte_msg)
    return pkcs1_15.new(RSA.import_key(public_key)).sign(hash)

def verify_key (message: str, signature: bytes, public_key: bytes) -> bool:
    hash = SHA256.new(message)
    try:
        pkcs1_15.new(public_key).verify(hash, signature)
        return True
    except (ValueError, TypeError):
        return False
    
# return Byte 
def export_new_rsa_key() -> bytes:
    key_pair = rsa_key_generator()
    public_key = key_pair.publickey().export_key()  # Export public key
    private_key = key_pair.export_key()  # Export private key
    return public_key, private_key

# return Byte
def encrypt_public_key(public_key: bytes, message: str) -> bytes: 
    byte_msg = message.encode('utf-8')
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    cipher_text = cipher_rsa.encrypt(byte_msg)
    return cipher_text

#r return String  
def decrypt_private_key (private_key: bytes, message: str):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    message = cipher_rsa.decrypt(message)
    return message.decode('utf-8')

def extract_rsa_key (key: str):
    return key[:258],key[258:]

def generate_key_to_str (key: bytes):
    return hex(key)

def generate_str_to_bytes (key: str):
    pass
