# Google
# import speech_recognition as sr
#
#
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Speak Anything :")
#         audio = r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         print("You said : {}".format(text))
#         listen()
#     except:
#         print("Sorry could not recognize what you said")
#         listen()
#
#
# listen()

# Sphynx
# import speech_recognition as sr
#
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Speak Anything :")
#         audio = r.listen(source)
#     try:
#         # Using Sphinx for recognition
#         text = r.recognize_sphinx(audio)
#         print("You said : {}".format(text))
#         listen()
#     except:
#         print("Sorry could not recognize what you said")
#         listen()
#
# listen()

# vosk:

import json
from vosk import Model, KaldiRecognizer
import os
import pyaudio
import threading

def listen_vosk():
    model = Model(r"C:\Users\jayaa\coding\Projects\virtual assistant\vosk-model-en-in-0.5")
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    print("started")

    def process_audio():
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                recognized_text = result.get('text', '').strip()
                if recognized_text:
                    print(recognized_text)

    # Start a separate thread to process audio
    audio_thread = threading.Thread(target=process_audio)
    audio_thread.start()

    # Wait for the audio processing to finish
    audio_thread.join()

    # Stop and close the audio stream and terminate the PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()

listen_vosk()


