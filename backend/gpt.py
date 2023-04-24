import json
from backend.utils import timeit
import time
import os
import openai
import user 


class GPTClient:
    # Constructor
    def __init__(
        self, 
        topic = '', # The topic of the conversation. '' if it is a free conversation
        chat_file='./data/chat.json', # The file where the conversation is written
        input_file="./data/input.txt", # The question of the user is read from this file
        output_file="./data/output.txt", # The answer of ChatGPT is written in this file to be converted to speech later
        initial_prompt_template="./data/starting_beginner_prompt_template.txt" # The conversation starts with a prompt that follows this template and is personnalized by the user info and level
    ):
        # Initiate model inference parameters to meet the user's level
        self.chooseTemperature()
        self.chooseTopP()
        self.chooseMaxTokens()
        self.choosefrequencePenalty()
        self.choosePresencePenalty()

        # Initiate the differente file paths
        self.input_file = input_file
        self.initial_prompt_template = initial_prompt_template
        self.output_file = output_file
        self.chat_file = chat_file
        self.topic = topic

        # Re initialize the chat file by deleting it if there is already a conversation inside or by creating it if it does not exist
        if os.path.exists(chat_file):
            os.remove(chat_file)
        with open(chat_file, 'w') as f:
            f.write('')

        # The question to chatGPT is read from the input file and saved in the question attribute 
        with open(input_file, "r") as f:
            self.question = f.read()

        # The answer is read from the output file if there is one and saved in the answer attribute 
        with open(output_file, "r") as f:
            self.answer = f.read()

        # Initial prompt is written to a new file from the intial prompt template file using user personal info and level
        self.writeInitialPromptFromTemplate(initial_prompt_template)
        
        # Initial prompt is read from the initial prompt file and saved in the initial_prompt attribute
        with open('./data/initial_prompt.txt', 'r') as f:
            self.initial_prompt = f.read()
        
        # Constructor ends

    # This function takes a template of an initial prompt of a chat and writes the initial prompt of the chat
    def writeInitialPromptFromTemplate(self, initial_prompt_template):
        
        # Template file is read
        f_template = open(initial_prompt_template, 'r')
        
        # Initial prompt file is instanciated
        f_user = open('./data/initial_prompt.txt', 'w')

        # Need to be modified! Not modular
        # Instanciation of the words that need to be changed in the template and the words that need to replace them
        template_words = ('$level', '$user_job', '$user_name', '$user_age', '$user_loc_city', '$user_loc_country')
        user_words = (user1.level, user1.userInfo['job'], user1.userInfo['name'], user1.userInfo['age'], user1.userInfo['location']['city'], user1.userInfo['location']['country'])
        
        # loop on lines in the template prompt
        for line in f_template:
            if 'Commence la conversation avec: ' in line: # Find the line that tell chatGPT how to start the chat
                    if self.topic != '': # If the user inputed a topic he wants the chat to talk about
                        # Replace the standard way to start the chat by the desired topic
                        f_user.write('Oriente la conversation autour du sujet suivant: ' + self.topic)
            else: # for every other line
                for check, rep in zip(template_words, user_words):
                    line = line.replace(check,rep) # replace the template word with the actual word
                    f_user.write(line)

        # Close files
        f_template.close()
        f_user.close()

    # Need to be updated! Values need to change with the user's level in a practical way
    # No particular algorithm so far
    def choosefrequencePenalty(self):
        if user1.level == 'beginner':
            self.frequence_penalty = -2
    
    def choosePresencePenalty(self):
        if user1.level == 'beginner':
            self.presence_penalty = 0
    
    def chooseMaxTokens(self):
        if user1.level == 'beginner':
            self.max_tokens = 200
    
    def chooseTemperature(self):
        if user1.level == 'beginner':
            self.temperature = 0.2 # 0:1
    
    def chooseTopP(self):
        if user1.level == 'beginner':
            self.top_p = 0.5 # 0:1 %

    # chatGPT api key instanciation
    def _api_key(self, config_file="./config.json"):
        with open(config_file, "r") as config:
            CONFIG = json.load(config)
        return CONFIG["openai_api_key"]

    @property
    def api_key(self):
        return self._api_key()

    # Inputs:
    # role in the chat (user, system)
    # content of message (a string)
    # Outputs:
    # returns a data structure to be added to the chat json file
    def formulate_message(self, role, content):
        return {"role": role, "content": content}

    # Write a new answer or question into the chat json file
    def store_chat(self, role, content):
        with open(self.chat_file, 'a') as f:
            json.dump(self.formulate_message(role, content), f)
            f.write('\n')

    # Reads the chat json file and returns a message data structure that is taken into argument by the model
    def retrieve_chat(self):
        with open(self.chat_file, 'r') as f:
            data = f.readlines()
        
        json_data = [json.loads(line.strip()) for line in data]

        messages = []
        for obj in json_data:
            messages.append(obj)
        return messages

    @timeit
    def ask_gpt(self, question) -> str:
        
        self.store_chat('user', question)
                
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature = self.temperature, # 0:1
            top_p = self.top_p, # 0:1, %
            max_tokens = self.max_tokens, #0:~4000
            n = 1,
            stream = True,
            presence_penalty  = self.presence_penalty, # -2:2
            frequency_penalty = self.frequence_penalty, # -2:2
            # logit_bias = json file - Modify the likelihood of specified tokens appearing in the completion.
            messages = self.retrieve_chat(),
        )

        collected_messages = []
        
        # Streaming capability not used
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)
        
        # Build the answer in a string format considering only the content of the message
        answer = ''.join([m.get('content', '') for m in collected_messages])
        self.store_chat("system", answer)  
        print(answer) 
        return answer

    def start_chat(self) -> None:
        self.ask_gpt(self.initial_prompt)

    def save_answer(self, answer) -> None:
        with open(self.output_file, "w") as f:
            f.write(answer)
 
    def run_agent(self):
        """run agent to run gpt request on entering"""

        while 1:
            self.ask_gpt(input("Ecrit ta réponse ici: "))
            time.sleep(1)


if __name__ == "__main__":
    user1 = user.User('Meir', 'beginner')
    gpt = GPTClient(input("De quoi souhaites tu discuter? "))
    
    openai.api_key = gpt.api_key
    gpt.start_chat()
    gpt.run_agent()
    # gpt.run_agent()
    # print(gpt.ask_gpt("Comment tu t'appelles"))
