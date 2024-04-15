# REMEMBER TO UPDATE Authenticate/hash.py when you update this file

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encode_password (password:str): 
    return password_context.hash(password)