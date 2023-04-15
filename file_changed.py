import os 
import time



with open("output.txt", "r") as f1: 
    input = f1.read()

while 1: 

    with open("output.txt", "r") as f1: 
        new_input = f1.read()
        if new_input != input: 
            start = time.time()
            print("file has changed")
            audio = gTTS(text=new_input, lang="he", slow=False)
            audio.save("speech.wav")
            os.system("afplay speech.wav")
            # outputs = synthesizer.tts(new_input)
            # synthesizer.save_wav(outputs, "speech.wav")
            end = time.time()
            input = new_input
            print(f"inference time: {end - start}")
        print("file has not changed")
        time.sleep(1)


            
    