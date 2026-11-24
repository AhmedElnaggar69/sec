import sys
import platform
import hashlib

print(f"Python {sys.version.split()[0]} on {platform.system()}\n")

# 1. Are all packages installed?
for pkg in ["cryptography", "sounddevice", "numpy", "matplotlib", "pytest"]:
    try:
        module = __import__(pkg)
        version = getattr(module, "__version__", "installed")
        print(f"[OK]   {pkg} {version}")
    except Exception as e:
        print(f"[FAIL] {pkg}: {e}")

# 2. Can Python see your microphone and speakers?
print("\nAudio devices:")
try:
    import sounddevice as sd
    print(sd.query_devices())
    print("Default (input, output):", sd.default.device)
except Exception as e:
    print(f"[FAIL] audio check: {e}")

# 3. A first taste of hashing
msg1 = b"Attack at dawn"
msg2 = b"Attack at dusk"
h1 = hashlib.sha256(msg1).hexdigest()
h2 = hashlib.sha256(msg2).hexdigest()
print("\nSHA-256 demo:")
print(msg1, "->", h1)
print(msg2, "->", h2)