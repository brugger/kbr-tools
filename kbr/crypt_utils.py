import secrets
import string

from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
import codecs

id_cipher = None

def init( id_secret:str) -> None:
    global id_cipher
    id_cipher = Blowfish.new(id_secret.encode('utf-8'), mode=Blowfish.MODE_ECB)


def decrypt_value(value:str) -> str:
    value_hex = codecs.decode(value, 'hex')
    decrypted_value = id_cipher.decrypt( value_hex ).decode("utf-8").lstrip("!")
    return decrypted_value

def encrypt_value(value:str) -> str:
    value = str( value )
    value = value.encode('utf-8')
    s = (b"!" * (8 - len(value) % 8)) + value
    # Encrypt
    return codecs.encode(id_cipher.encrypt(s), 'hex').decode("utf-8")


def create_uuid(length=16):
    # Generate a unique, high entropy random number.
    # Length 16 --> 128 bit 
    return codecs.encode(get_random_bytes(length), 'hex').decode("utf-8")

def create_guid():
    return create_uuid()


def create_password(length=12) -> str:
    if length<=8:
        raise RuntimeError("password length is to short. 8 chars is the minumum")
    special_chars = "@#$%^&*-_"
    alphabet = string.ascii_letters + string.digits + special_chars
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
           and any(c.isupper() for c in password)
           and any(c in special_chars for c in password)
           and sum(c.isdigit() for c in password) >= 3):
            break

    return password
