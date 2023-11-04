from PyQt5.QtCore import pyqtSignal, QThread
import orjson
from vosk import Model, KaldiRecognizer
import pyaudio


class STT(QThread):
    user_spoke = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        model = Model(r"vosk-model-en-in-0.5")
        self.rec = KaldiRecognizer(model, 16000)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
        self.stream.start_stream()
        print("started mic stream")

        # Add a flag to indicate whether voice recognition should continue
        self.keep_listening = False

    def run(self):
        while self.keep_listening:
            data = self.stream.read(4096, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result = orjson.loads(self.rec.Result())
                recognized_text = result.get('text', '').strip()
                if recognized_text:
                    self.user_spoke.emit(recognized_text)

    def stop(self):
        # Stop and close the audio stream and terminate the PyAudio instance
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
