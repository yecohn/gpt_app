import requests
import time
import sys
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

# Sampling frequency
freq = 44100

# Recording duration
duration = 5
#  Start recorder with the given values of
# duration and sample frequency
print("start recording")
recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

# Record audio for the given number of seconds
sd.wait()
print("end recording")
write("tmp.wav", freq, recording)
wv.write("tmp.wav", recording, freq, sampwidth=2)


API_TOKEN = "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"
API_URL = (
    "https://api-inference.huggingface.co/models/qanastek/whisper-tiny-french-cased"
)

headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


start = time.time()
output = query("tmp.wav")
end = time.time()
print(output)
hard_coded_prompt = "\n fais moi 2 phrases et une question."
# if "text" not in output.keys():
#     print("model endpoint is not ready for use")
#     sys.exit()
# output = output["text"] + hard_coded_prompt
print(f"inference time: {end - start}")
with open("input.txt", "w") as f1:
    print(output["text"])
    f1.write(output["text"])
