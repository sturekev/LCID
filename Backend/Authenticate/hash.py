import bcrypt

def encodePassword ():
    pass 

# password = "my_password".encode('utf-8')
# print (password)
# bcrypt.gensalt()s
password = "my_password".encode('utf-8')  # Convert the password to bytes

# Hash the password
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
def encodePassword (password:str): 
    return password.encode('utf-8')

def hashedPassword (endcodePassword):
    return bcrypt.hashpw(endcodePassword, bcrypt.gensalt())

def checkPassword (endcodePassword, hashed: bytes):
    if bcrypt.checkpw(endcodePassword, hashed):
        return True
    return False
