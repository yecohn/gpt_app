from google.cloud import texttospeech
from fastapi.responses import FileResponse


class TTS:
    def __init__(
        self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code = "es-ES",
            ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    
    def generate_speech(self, text):

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Select the type of audio file you want returned

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        # The response's audio_content is binary.
        audio_file = 'output.m4a'
        with open(audio_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file {audio_file}')
        return audio_file


# class BaseTTS:
#     @abstractclassmethod
#     def generate_speech():
#         pass


# class GCPTTS(BaseTTS):
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3,
#         # TODO: hardcoded need to change this
#         speaking_rate=1,
#     )

#     def __init__(self, language, speaker):
#         self.language = language
#         self.speaker = speaker
#         self.client = texttospeech.TextToSpeechClient()

#     @property
#     def voice(self):
#         return texttospeech.VoiceSelectionParams(
#             language_code=self.language,
#             name=self.speaker,
#             ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
#         )

#     @timeit
#     def generate_speech(
#         self, text, audio_path="./frontend/src/assets/speech.mp3"
#     ) -> None:
#         """from input file generate speech mp3 file and save it into audio_path
#         Args:
#             audio_path (str, optional):. Defaults to '../data/speech.mp3'.
#         """
#         synthesis_input = texttospeech.SynthesisInput(text=text)
#         response = self.client.synthesize_speech(
#             input=synthesis_input, voice=self.voice, audio_config=self.audio_config
#         )
#         with open(audio_path, "wb") as out:
#             out.write(response.audio_content)
