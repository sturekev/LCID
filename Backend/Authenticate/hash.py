import bcrypt

def encodePassword (password:str): 
    return password.encode('utf-8')

def hashedPassword (endcodePassword):
    return bcrypt.hashpw(endcodePassword, bcrypt.gensalt())

def checkPassword (endcodePassword, hashed: bytes):
    if bcrypt.checkpw(endcodePassword, hashed):
        return True
    return False
