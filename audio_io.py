import wave
import numpy as np
import sounddevice as sd
import sys

sampleRate = 16000 # waves per sec
channels = 1 # one micro
dtype = "int16" # each sample is 16 bit number (2 bytes)
bytesPerSample = 2

inputDevice = None
ouputDevice = None


def record(secs):
    # record from mico and return audio as bytes
    print(f"recording for {secs} seconds (SPEAK NOW!!)")
    audio = sd.rec(
        int(secs*sampleRate) , 
        samplerate=sampleRate,
        channels=channels,
        dtype=dtype ,
        device = inputDevice)
    
    sd.wait() # wait until recording is done
    
    print("done recording")
    return audio.tobytes() # turns numpy array to bytes

def save_wav(bytes , filename):
    # write audio bytes to wav file
    
    with wave.open(filename , "wb") as f:
        f.setnchannels(channels)
        f.setsampwidth(bytesPerSample)
        f.setframerate(sampleRate)
        f.writeframes(bytes)

def load_wav(filename):
    with wave.open(filename , "rb") as f:
        if (f.getframerate() != sampleRate
            or f.getnchannels() != channels or
            f.getsampwidth()!= bytesPerSample
            ):
            raise ValueError("wav file does not match our audio settings")
        return f.readframes(f.getnframes()) 
    
def play(bytes):
    audio = np.frombuffer(bytes , dtype=dtype) # bytes to array again
    print(f"playing {len(audio) /sampleRate:.1f} seconds of audio")
    sd.play(audio , samplerate=sampleRate , device=ouputDevice)
    
    
if __name__ == "__main__":
    secs = int(sys.argv[1])
    
    data = record(secs)
    
    samples = np.frombuffer(data , dtype=dtype)
    save_wav(data , "message.wav")
    loaded = load_wav("message.wav")
    
    play(loaded)