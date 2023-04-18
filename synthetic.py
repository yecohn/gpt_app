from pydub import AudioSegment
import os
from pydub.playback import play
import time

# TOKEN = "XqXlo60K4SwlgtCgkjlziuMY2aAwT7jdbN55TqTOHccTxJlq3wbQ9WJ7K6JLFvjq"
# os.environ["COQUI_STUDIO_TOKEN"] = TOKEN
OUTPUT_PATH = "speech.wav"


wav_file = AudioSegment.from_wav(OUTPUT_PATH)
while 1:
    song = AudioSegment.from_wav(OUTPUT_PATH)
    if song != wav_file:
        print("song play")
        play(song)
        wav_file = song
    print("song not play")
    time.sleep(1)
