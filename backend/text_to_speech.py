import os 
import time
from gtts import gTTS
from backend.utils import timeit


class TTS(): 
    def __init__(self, output_file="./data/output.txt", tts_algo=gTTS): 
        self.output_file = output_file
        self.tts_algo = tts_algo

    @property
    def input(self): 
        with open("./data/output.txt", "r") as f1: 
            return f1.read()

    @timeit
    def generate_speech(self, audio_path='./data/speech.wav') -> None: 
        """from input file generate speech wav file and save it into audio_path

        Args:
            audio_path (str, optional):. Defaults to '../data/speech.wav'.
        """
        with open(self.output_file, "r") as f1: 
            new_input = f1.read()
            if new_input != self.input: 
                print("file has changed")
                audio = self.tts_algo(text=new_input, lang="fr", slow=False)
                audio.save(audio_path)
                os.system(f"afplay {audio_path} ")
                self.input = new_input

    


    # def run_agent(self):
    #     while True:
    #         self.generate_speech()
    #         time.sleep(1)






            
    