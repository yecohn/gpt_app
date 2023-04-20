import os
import time
from gtts import gTTS
from backend.utils import timeit


class TTS:
    def __init__(self, output_file="./data/output.txt", tts_algo=gTTS):
        self.output_file = output_file
        self.tts_algo = tts_algo

    @property
    def input(self):
        with open("./data/output.txt", "r") as f1:
            return f1.read()

    @timeit
    def generate_speech(self, text, audio_path="../data/speech.wav") -> None:
        """from input file generate speech wav file and save it into audio_path

        Args:
            audio_path (str, optional):. Defaults to '../data/speech.wav'.
        """

        audio = self.tts_algo(text=text, lang="fr", slow=False)
        audio.save(audio_path)
        return audio_path
