import json
from backend.utils import timeit
import time
import os
import openai
import enum
from typing import Dict, List
from backend.user import User


class GPTClient:
    def __init__(
        self,
        user: User,
    ):
        self.user = user

    @property
    def metadata(self):
        return self._metadata()

    def _metadata(self):
        with open("backend/db.json", "r") as f:
            _metadata = json.load(f).get("GPT_metadata")
        return _metadata

    @property
    def level(self):
        user_level = self.user.level.upper()
        return Level.__members__[user_level].value

    def initialize_chat(self) -> None:
        """
        Re initialize the chat file by deleting it if there is already a
        conversation inside or by creating it if it does not exist
        """
        chat_file = self.metadata.get("chat_file")
        if os.path.exists(chat_file):
            os.remove(chat_file)
        initial_prompt = self.initial_prompt
        self.store_chat(role="user", content=initial_prompt)

    @property
    def question(self) -> str:
        """load question from input file"""
        with open(self.metatadata.get("input_file"), "r") as f:
            question = f.read()
        return question

    @question.setter
    def question(self, question):
        with open(self.metadata.get("input_file"), "w") as f:
            f.write(question)

    @property
    def answer(self) -> str:
        with open(self.metadata.get("output_file"), "r") as f:
            answer = f.read()
        return answer

    @answer.setter
    def answer(self, answer):
        with open(self.metadata.get("output_file"), "w") as f:
            f.write(answer)

    @property
    def initial_prompt(self):
        with open(self.metadata.get("initial_prompt_template"), "r") as f_template:
            attributes = ("level", "job", "name", "age", "city", "country")
            user_words = {attr: self.user.__getattribute__(attr) for attr in attributes}
            template_text = f_template.read().format(**user_words)
        return template_text

    def _api_key(self, config_file="./config.json"):
        with open(config_file, "r") as config:
            CONFIG = json.load(config)
        return CONFIG["openai_api_key"]

    @property
    def api_key(self):
        return self._api_key()

    def formulate_message(self, role: str, content: str) -> Dict:
        """
        Args:
            role (str): role in chat
            content (str): content of message

        Returns:
            dict: returns a dict to be added to the chat json file
        """
        return {"role": role, "content": content}

    def store_chat(self, role: str, content: str) -> None:
        """
         Write a new answer or question into the chat json file
        Args:
            role (str):
            content (str):
        """
        with open(self.metadata.get("chat_file"), "a") as f:
            json.dump(self.formulate_message(role, content), f)
            f.write("\n")

    def retrieve_chat(self) -> List[Dict]:
        """
        Reads the chat json file and returns a message data structure that is taken into argument by the model
        Returns: List[Dict]: List of messages to be processed by gpt api
        """
        with open(self.metadata.get("chat_file"), "r") as f:
            data = f.readlines()
        json_data = [json.loads(line.strip()) for line in data]
        messages = []
        for obj in json_data:
            messages.append(obj)
        return messages

    @timeit
    def ask_gpt(self, question) -> str:
        """ask gpt a question and get an answer
        Args:
            question (str): question to be asked

        Returns:
            str: answer to the question
        """
        self.question = question
        self.store_chat("user", question)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=self.level.get("temperature"),  # 0:1
            top_p=self.level.get("top_p"),  # 0:1, %
            max_tokens=self.level.get("max_tokens"),  # 0:~4000
            n=1,
            stream=True,
            presence_penalty=self.level.get("presence_penalty"),  # -2:2
            frequency_penalty=self.level.get("frequence_penalty"),  # -2:2
            # logit_bias = json file - Modify the likelihood of specified tokens appearing in the completion.
            messages=self.retrieve_chat(),
        )
        collected_messages = []
        # Streaming capability not used
        for chunk in response:
            chunk_message = chunk["choices"][0]["delta"]
            collected_messages.append(chunk_message)

        # Build the answer in a string format considering only the content of the message
        answer = "".join([m.get("content", "") for m in collected_messages])
        self.store_chat("system", answer)
        self.answer = answer
        return answer

    # nee to use files input and output instead entry message
    def start_chat(self) -> None:
        """start conversation by submitting first question to gpt"""
        self.ask_gpt(question="")

    def save_answer(self, answer: str) -> None:
        """save answer to file for later use"""
        with open(self.output_file, "w") as f:
            f.write(answer)

    def run_agent(self):
        """run agent to run gpt request on entering"""

        while 1:
            self.ask_gpt(input("Ecrit ta réponse ici: "))
            time.sleep(1)


class Level(enum.Enum):
    BEGINNER = {
        "frequence_penalty": -2,
        "presence_penalty": 0,
        "max_tokens": 200,
        "temperature": 0.2,
        "top_p": 0.5,
    }


if __name__ == "__main__":
    user1 = User("Meir")
    gpt = GPTClient(
        user=user1,
    )
    openai.api_key = gpt.api_key
    # gpt.initialize_chat()
    print(gpt.ask_gpt("C'est un passage incroyable ! "))
