"""demo_step3.py - why encryption alone is not enough, and how HMAC fixes it."""
import hashlib

import audio_io
from crypto.aes_layer import generate_key, encrypt, decrypt
from crypto.hmac_layer import generate_mac_key, compute_tag, verify_tag

plaintext = audio_io.load_wav("message.wav")
aes_key = generate_key()
mac_key = generate_mac_key()

# ---- ALICE: encrypt, then tag nonce + ciphertext ----
nonce, ciphertext = encrypt(aes_key, plaintext)
tag = compute_tag(mac_key, nonce + ciphertext)
print(f"Tag (hex): {tag.hex()}")

# ---- MALLORY: changes ONE byte in the middle of the ciphertext ----
position = len(ciphertext) // 2
tampered = bytearray(ciphertext)   # bytearray = bytes you are allowed to edit
tampered[position] ^= 0xFF         # XOR with 255 flips all 8 bits of that byte
tampered = bytes(tampered)

# ---- PART 1: Bob has AES only ----
recovered = decrypt(aes_key, nonce, tampered)
changed = [i for i in range(len(plaintext)) if recovered[i] != plaintext[i]]
print("\n--- AES only ---")
print("decrypt finished with no error")
print(f"Bytes that differ from the original: {len(changed)} (positions: {changed})")

# ---- PART 2: Bob has AES + HMAC ----
bad_nonce = bytes([nonce[0] ^ 1]) + nonce[1:]   # flip one bit of the nonce

print("\n--- AES + HMAC ---")
print("Untouched message accepted?   ", verify_tag(mac_key, nonce + ciphertext, tag))
print("Tampered ciphertext accepted? ", verify_tag(mac_key, nonce + tampered, tag))
print("Tampered nonce accepted?      ", verify_tag(mac_key, bad_nonce + ciphertext, tag))
print("Wrong MAC key accepted?       ", verify_tag(generate_mac_key(), nonce + ciphertext, tag))
print("Truncated tag accepted?       ", verify_tag(mac_key, nonce + ciphertext, tag[:16]))

# ---- PART 3: could Mallory just forge a tag with plain SHA-256? ----
forged = hashlib.sha256(nonce + tampered).digest()
print("Mallory's plain-hash forgery accepted?", verify_tag(mac_key, nonce + tampered, forged))