

import openai
import sounddevice as sd
import wavio as wv
from google.cloud import speech
import os
from backend.gpt import GPTClient
from backend.speech_to_text import STT
from backend.text_to_speech import TTS
import streamlit as st
import base64
from sound import Sound

gpt = GPTClient()
tts = TTS()
client = speech.SpeechClient()
freq = 44100
duration = 5
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=1,
    language_code="fr-FR",
)
recording_path = "../data/tmp.wav"
recording_input_path = "../data/input.wav"

stt = STT(
    stt_client=client,
    stt_service=speech.RecognitionAudio,
    stt_config=config,
    freq=freq,
    duration=duration,
    recording_path=recording_path,
)
openai.api_key = gpt.api_key


sound = Sound()
WAVE_OUTPUT_FILE = "./output/recording/recorded.wav"
WAVE_ANSWER_PATH = "./output/recording/answer.wav"


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


def main(transcript, answer):
    title = "Apprentissage Francais Interactif"

    st.title(title)

    if st.button("Record"):
        with st.spinner(f"Recording for {5} seconds ...."):
            sound.record()
        transcript, encoded_prompt = stt.get_transcript_from_recording(WAVE_OUTPUT_FILE)
        print(transcript, encoded_prompt)
        full_prompt = "".join((transcript, encoded_prompt))
        answer = gpt.ask_gpt(full_prompt)
        tts.generate_speech(answer, WAVE_ANSWER_PATH)
        autoplay_audio(WAVE_ANSWER_PATH)
        st.success("Recording completed")

    if st.button("Play"):
        # sound.play()
        audio_file = open(WAVE_ANSWER_PATH, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/wav", start_time=0)

    if answer == "":
        st.header("gpt prompt")
        st.markdown("tu peux me demander qqchose")
    else:
        st.header("gpt prompt")
        st.markdown(answer)

    if transcript == "":
        st.header("user prompt")
        st.markdown("encore rien demander")
    else:
        st.header("user prompt")
        st.markdown(transcript)

    # st.markdown("user prompt: " + transcript)


if __name__ == "__main__":
    transcript = ""
    answer = ""
    main(transcript, answer)
    