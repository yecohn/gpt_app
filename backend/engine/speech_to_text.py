import openai
from fastapi import UploadFile

class STT:
    def __init__(self) -> None:
        self._uploaded_audio = None

    @property
    def uploaded_audio(self):
        return self._uploaded_audio
    
    @uploaded_audio.setter
    def uploaded_audio(self, audio_file: UploadFile):
        self._uploaded_audio = audio_file
        
    @classmethod
    def transcript(cls, uploaded_audio: UploadFile) -> str:
        print('Starting speech to text transcription...')
        trancription = openai.Audio.transcribe(uploaded_audio)
        return trancription['text']


# import sounddevice as sd
# import wavio as wv
# from google.cloud import speech
# import os
# import io
# from typing import Type
# import numpy as np

# # os.environ[
# #     "GOOGLE_APPLICATION_CREDENTIALS"
# # ] = "/Users/yosh/Desktop/gpu-machine-383109-eb6f06eb9e8a.json"


# class STT:
#     def __init__(
#         self,
#         stt_client: speech.SpeechClient,
#         stt_service: Type[speech.RecognitionAudio],
#         stt_config: speech.RecognitionConfig,
#         freq: int = 44100,
#         duration: int = 5,
#         recording_path: str = "../data/tmp.wav",
#     ):
#         self.stt_client = stt_client
#         self.stt_service = stt_service
#         self.stt_config = stt_config
#         self.freq = freq
#         self.duration = duration
#         self.recording_path = recording_path

#     def record_message(self) -> None:
#         print("start recording")
#         recording = sd.rec(
#             int(self.duration * self.freq), samplerate=self.freq, channels=1
#         )
#         print(type(recording))
#         sd.wait()
#         print("end recording")
#         self.write_recording(recording)

#     def write_recording(self, recording):
#         wv.write(self.recording_path, recording, self.freq, sampwidth=2)

#     def load_recording(self, recording_path=None):
#         if not recording_path:
#             with io.open(self.recording_path, "rb") as recorded_file:
#                 return recorded_file.read()

#         with io.open(recording_path, "rb") as recorded_file:
#             return recorded_file.read()

#     def get_transcript_from_recording(self, recording_path=None):
#         data = self.load_recording(recording_path)
#         audio = self.stt_service(content=data)

#         response = self.stt_client.recognize(
#             request={"config": self.stt_config, "audio": audio}
#         )

#         # Reads the response
#         transcript = []
#         for result in response.results:
#             transcript += result.alternatives[0].transcript
#         transcript = "".join(transcript)
#         return transcript

#     def save_transcript(self, transcript, output_path):
#         with open(output_path, "w") as transcript_file:
#             transcript_file.write(transcript)

#     def record_and_transcript(self):
#         self.record_message()
#         transcript = self.get_transcript_from_recording()
#         return transcript


# if __name__ == "__main__":
#     client = speech.SpeechClient()
#     freq = 44100
#     duration = 5
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         audio_channel_count=1,
#         language_code="iw-IL",
#     )
#     recording_path = "../data/tmp.wav"

#     stt = STT(
#         stt_client=client,
#         stt_service=speech.RecognitionAudio,
#         stt_config=config,
#         freq=freq,
#         duration=duration,
#         recording_path=recording_path,
#     )
#     transcript = stt.record_and_transcript()
#     print(transcript)
