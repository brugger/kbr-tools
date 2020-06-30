from Crypto.Cipher import Blowfish
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
    value = value.encode('utf-8')
    s = (b"!" * (8 - len(value) % 8)) + value
    # Encrypt
    return codecs.encode(id_cipher.encrypt(s), 'hex').decode("utf-8")

