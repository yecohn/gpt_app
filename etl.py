# %%
from pydub import AudioSegment
import pandas as pd
import os
import re
from tqdm import tqdm

# importing file from location by giving its path
DATA_PATH = "/Users/yosh/Downloads/nebsu"
AUDIO_FILE = "nebsu1.mp3"
LABEL_FILE = "nebsu1_label.xlsx"

# %%
sound = AudioSegment.from_mp3(os.path.join(DATA_PATH, AUDIO_FILE))
df = pd.read_excel(os.path.join(DATA_PATH, LABEL_FILE))


# Saving file in required location
# %%
# convert time to time object
def convert_second_to_number(str_time):
    if str_time[-1] == "s":
        tmp = str_time[:-1]
        if len(tmp) == 2:
            str_time = f"00:{tmp}"
        elif len(tmp) == 1:
            str_time = f"00:0{tmp}"
        else:
            raise ValueError
    return str_time


def convert_time_to_millisecond(str_time):
    minute, second = str_time.split(":")
    minute = int(minute)
    second = int(second)
    time = minute * 60 * 1000 + second * 1000
    return time


def create_portion(start, end):
    return sound[start:end]


df["Time"] = df["Time"].apply(lambda x: convert_second_to_number(x))
df["time_mili"] = df["Time"].apply(lambda x: convert_time_to_millisecond(x))
df["time_mili_next"] = df["time_mili"].shift(-1)
df.dropna(inplace=True)
df["portion"] = df[["time_mili", "time_mili_next"]].apply(
    lambda x: create_portion(*x), axis=1
)
df
# %%
subtitles = df["Subtitle"].values
portions = df["portion"].values

for i, subtitle in tqdm(enumerate(subtitles)):
    dir_path = os.path.join(f"{DATA_PATH}", "data")
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, f"{i+1}.txt"), "w") as f:
        f.write(subtitle)


for i, portion in tqdm(enumerate(portions)):
    dir_path = os.path.join(f"{DATA_PATH}", "data")
    os.makedirs(dir_path, exist_ok=True)
    portion.export(os.path.join(dir_path, f"{i+1}.mp3"), format="mp3")


# %%
# new file portion.mp3 is saved at required location
