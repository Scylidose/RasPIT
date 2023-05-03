import pvporcupine
import pyaudio
import struct
import io
import wave
import requests
from pygame import mixer

def process_audio_after_wake_word():
    # Set up the audio recording parameters
    RECORD_SECONDS = 4
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    # Set up PyAudio for recording
    audio = pyaudio.PyAudio()

    # Start recording
    print("Recording...")
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio as a WAV file in memory
    wav_file = io.BytesIO()
    with wave.open(wav_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    wav_file.seek(0)

    # Send the audio file to the Flask app
    print("Sending audio to the server...")
    response = requests.post('http://localhost:5000/process_audio', files={'audio_file': wav_file})

    if response.status_code == 200:
        result = response.json()
        response_text = result['response_text']
        response_audio = result['response_audio']

        # Download the response audio
        audio_data = requests.get(response_audio).content

        # Save the response audio as a temporary file
        with open('temp_response.mp3', 'wb') as f:
            f.write(audio_data)

        # Play the response audio using pygame.mixer
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
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=["raspit"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
            input_device_index=None,
        )

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected")
                process_audio_after_wake_word()

    except KeyboardInterrupt:
        print("Stopping")

    finally:
        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()

        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    main()
