import os
import time
from gtts import gTTS
from backend.utils import timeit
from google.cloud import texttospeech
from abc import ABC, abstractclassmethod


class BaseTTS:
    @abstractclassmethod
    def generate_speech():
        pass


class GCPTTS(BaseTTS):
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    def __init__(self, language, speaker):
        self.language = language
        self.speaker = speaker
        self.client = texttospeech.TextToSpeechClient()

    @property
    def voice(self):

        return texttospeech.VoiceSelectionParams(
            language_code=self.language,
            name=self.speaker,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

    @timeit
    def generate_speech(
        self, text, audio_path="./frontend/src/assets/speech.mp3"
    ) -> None:
        """from input file generate speech mp3 file and save it into audio_path
        Args:
            audio_path (str, optional):. Defaults to '../data/speech.mp3'.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        with open(audio_path, "wb") as out:
            out.write(response.audio_content)
