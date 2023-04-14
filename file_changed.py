import os 
import time
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import site
location = site.getsitepackages()[0]
from gtts import gTTS

path = location+"/TTS/.models.json"

# model_manager = ModelManager(path)

# model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

# voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

# synthesizer = Synthesizer(
#     tts_checkpoint=model_path,
#     tts_config_path=config_path,
#     vocoder_checkpoint=voc_path,
#     vocoder_config=voc_config_path
# )


with open("output.txt", "r") as f1: 
    input = f1.read()

while 1: 

    with open("output.txt", "r") as f1: 
        new_input = f1.read()
        if new_input != input: 
            start = time.time()
            print("file has changed")
            audio = gTTS(text=new_input, lang="en", slow=False)
            audio.save("speech.wav")
            os.system("afplay speech.wav")
            # outputs = synthesizer.tts(new_input)
            # synthesizer.save_wav(outputs, "speech.wav")
            end = time.time()
            input = new_input
            print(f"inference time: {end - start}")
        print("file has not changed")
        time.sleep(1)


            
    