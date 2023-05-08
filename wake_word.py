import sys
from dotenv import load_dotenv
import os

load_dotenv()

porcupine_path = os.getenv("PATH_TO_PORCUPINE")

sys.path.append(porcupine_path)

import pvporcupine
import struct
import io
import wave
import requests
import time 

import sounddevice as sd
import numpy as np

def process_audio_after_wake_word():
    RECORD_SECONDS = 4
    RATE = 16000

    print("Recording...")
    recording = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=1, dtype=np.int16)
    sd.wait()
    
    wav_file = io.BytesIO()
    wavio.write(wav_file, recording, RATE, sampwidth=2)
    wav_file.seek(0)

    print("Sending audio to the server...")
    response = requests.post('http://localhost:5000/process_audio', files={'audio_file': wav_file})

    if response.status_code == 200:
        result = response.json()
        response_text = result['response_text']
        response_audio = result['response_audio']

        audio_data = requests.get(response_audio).content

        with open('temp_response.mp3', 'wb') as f:
            f.write(audio_data)

        mixer.init()
        mixer.music.load('temp_response.mp3')
        mixer.music.play()

        while mixer.music.get_busy():
            continue

        print("Response:", response_text)

    else:
        print("Error:", response.status_code)

def main():
    porcupine = None
    audio_stream = None

    try:
        access_key = os.getenv("ACCES_TOKEN_PORCUPINE")

        porcupine = pvporcupine.create(keywords=["jarvis"], access_key=access_key)
        
        def callback(indata, frames, time, status):
            if status:
                print("Error:", status)
            pcm = indata.flatten()
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected")
                process_audio_after_wake_word()

        with sd.InputStream(
            samplerate=porcupine.sample_rate,
            channels=1,
            dtype=np.int16,
            blocksize=porcupine.frame_length,
            callback=callback
        ):
            print("Listening for wake word...")
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping")

    finally:
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    main()
