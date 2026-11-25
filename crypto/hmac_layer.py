import hashlib 
import hmac
import os

MAC_KEY_SIZE = 32   # 32 bytes = 256 bits, separate from the AES key
TAG_SIZE = 32       # SHA-256 produces 32 bytes

def generate_mac_key():
    return os.urandom(MAC_KEY_SIZE)

def compute_tag(mac_key, data):
    # returns the 32-byte tag for the given data
    if len(mac_key) != MAC_KEY_SIZE:
        raise ValueError(f"MAC key must be {MAC_KEY_SIZE} bytes, got {len(mac_key)}")
    return hmac.new(mac_key, data, hashlib.sha256).digest()

def verify_tag(mac_key, data, tag):
    expected = compute_tag(mac_key, data)
    return hmac.compare_digest(expected, tag)