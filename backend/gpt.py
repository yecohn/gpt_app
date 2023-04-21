import json
from backend.utils import timeit
import time

import openai
import user 


class GPTClient:
    def __init__(
        self, input_file="./data/input.txt", output_file="./data/output.txt", initial_prompt_template="./data/starting_beginner_prompt_template.txt"
    ):
        self.chooseTemperature()
        self.chooseTopP()
        self.chooseMaxTokens()
        self.choosefrequencePenalty()
        self.choosePresencePenalty()
        self.input_file = input_file
        self.initial_prompt_template = initial_prompt_template
        self.output_file = output_file

        with open(input_file, "r") as f:
            self.question = f.read()

        with open(output_file, "r") as f:
            self.answer = f.read()

        self.writeInitialPromptFromTemplate(initial_prompt_template)
        f = open('initial_prompt.txt', 'r')
        self.initial_prompt = f.read()
        f.close()
        # with open(initial_beginner_prompt_file, "r") as f:
        #     self.chat_starting_prompt = f.read()

    def writeInitialPromptFromTemplate(self, initial_prompt_template):
        f_template = open(initial_prompt_template, 'r')
        f_user = open('initial_prompt.txt', 'w')
        template_words = ('$level', '$user_job', '$user_name', '$user_age', '$user_loc_city', '$user_loc_country')
        user_words = (user1.level, user1.userInfo['job'], user1.userInfo['name'], user1.userInfo['age'], user1.userInfo['location']['city'], user1.userInfo['location']['country'])
        for line in f_template:
            for check, rep in zip(template_words, user_words):
                line = line.replace(check,rep)
            f_user.write(line)
        f_template.close()
        f_user.close()
        
    def choosefrequencePenalty(self):
        if user1.level == 'beginner':
            self.frequence_penalty = -2
    
    def choosePresencePenalty(self):
        if user1.level == 'beginner':
            self.presence_penalty = 0
    
    def chooseMaxTokens(self):
        if user1.level == 'beginner':
            self.max_tokens = 50
    
    def chooseTemperature(self):
        if user1.level == 'beginner':
            self.temperature = 0.2 # 0:1
    
    def chooseTopP(self):
        if user1.level == 'beginner':
            self.top_p = 0.5 # 0:1 %

    def _api_key(self, config_file="./config.json"):
        with open(config_file, "r") as config:
            CONFIG = json.load(config)
        return CONFIG["openai_api_key"]

    @property
    def api_key(self):
        return self._api_key()

    @timeit
    def ask_gpt(self, question) -> str:

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
            messages=[
                {"role": "system", "content": "You are Christian, my conversation partner to learn French", "name": "Christian"},
                {"role": "user", "content": question},
            ],
        )

        collected_messages = []
        
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)
        
        answer = ''.join([m.get('content', '') for m in collected_messages])
                
        return answer

    def start_conversation(self) -> None:
        answer = self.ask_gpt(self.initial_prompt)
        print(answer)

    def save_answer(self, answer) -> None:
        with open(self.output_file, "w") as f:
            f.write(answer)
 
    def run_agent(self):
        """run agent to run gpt request on entering"""

        while 1:
            self.ask_gpt()
            time.sleep(1)


if __name__ == "__main__":
    user1 = user.User('Meir', 'beginner')
    gpt = GPTClient()
    
    openai.api_key = gpt.api_key
    gpt.start_conversation()
    # gpt.run_agent()
    # print(gpt.ask_gpt("Comment tu t'appelles"))
