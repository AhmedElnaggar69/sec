import os

from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes

key_size = 32 # 32 bytes = 256 bits
nonce_size = 16 # input size

def generate_key():
    # make a fresh random 256-bit key
    return os.urandom(key_size)

def encrypt(key , plaintext):
    # returns nonce and cipher text
    if len(key)!=key_size:
        raise ValueError(f"key must be the same size as the key size: {key_size} you got a {len(key)} sized key")
    
    nonce = os.urandom(nonce_size)
    
    cipher = Cipher(algorithms.AES(key) , modes.CTR(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return nonce, ciphertext

def decrypt(key , nonce , ciphertext):
    if len(key)!=key_size:
        raise ValueError(f"key must be the same size as the key size: {key_size} you got a {len(key)} sized key")
        
    cipher = Cipher(algorithms.AES(key) , modes.CTR(nonce))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()