import os 
import time
with open("input.txt", "r") as f1: 
    input = f1.read()

while 1: 

    with open("input.txt", "r") as f1: 
        new_input = f1.read()
        if new_input != input: 
            print("file has changed")
            os.system('tts --text "$(cat input.txt)" --out_path speech.wav')
            input = new_input
        print("file has not changed")
        time.sleep(2)


            
    