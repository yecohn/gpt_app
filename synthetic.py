from TTS.api import TTS
from pydub import AudioSegment
import os
from pydub.playback import play
import time

TOKEN = "XqXlo60K4SwlgtCgkjlziuMY2aAwT7jdbN55TqTOHccTxJlq3wbQ9WJ7K6JLFvjq"
os.environ["COQUI_STUDIO_TOKEN"] = TOKEN
OUTPUT_PATH = "speech.wav"

# tts = TTS(model_name="tts_models/en/ek1/tacotron2", progress_bar=False, gpu=False)
# tts.tts_to_file(
#     text="hi there, how are you today ? ",
#     file_path=OUTPUT_PATH,
# )


wav_file = AudioSegment.from_wav(OUTPUT_PATH)
while 1:
    song = AudioSegment.from_wav(OUTPUT_PATH)
    if song != wav_file:
        print("song play")
        play(song)
        wav_file = song
    print("song not play")
    time.sleep(1)
