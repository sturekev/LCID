# REMEMBER TO UPDATE Authenticate/hash.py when you update this file

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encodePassword (password:str): 
    return pwd_context.hash(password)