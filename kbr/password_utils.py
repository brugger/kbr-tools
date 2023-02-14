import hashlib
import uuid

def hash_password(password:str, salt:str=None):
    # uuid is used to generate a random number
    if salt is None:
        salt = uuid.uuid4().hex

    return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()

