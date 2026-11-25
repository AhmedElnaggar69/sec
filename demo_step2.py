"""demo_step2.py - try the AES layer on the real voice message."""
import time

import audio_io
from crypto.aes_layer import generate_key, encrypt, decrypt

# 1. Load the voice message (raw audio bytes)
plaintext = audio_io.load_wav("message.wav")
print(f"Plaintext size : {len(plaintext)} bytes")

# 2. Make a key and encrypt
key = generate_key()
print(f"Key (hex)      : {key.hex()}")

start = time.perf_counter()
nonce, ciphertext = encrypt(key, plaintext)
elapsed = time.perf_counter() - start

print(f"Nonce (hex)    : {nonce.hex()}")
print(f"Ciphertext size: {len(ciphertext)} bytes")
print(f"Encryption took: {elapsed * 1000:.1f} ms")

# 3. Compare the first 16 bytes before and after
print(f"\nFirst 16 plaintext bytes : {plaintext[:16].hex()}")
print(f"First 16 ciphertext bytes: {ciphertext[:16].hex()}")

# 4. Decrypt with the right key and check we got the original back
recovered = decrypt(key, nonce, ciphertext)
print("\nDecrypted == original?", recovered == plaintext)

# 5. Hear what Mallory would hear
audio_io.save_wav(ciphertext, "ciphertext_noise.wav")
print("\nPlaying the ciphertext as if it were audio...")
audio_io.play(ciphertext)

# 6. Hear the real message coming back
print("Playing the decrypted message...")
audio_io.play(recovered)