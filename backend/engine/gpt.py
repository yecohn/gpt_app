import json
import time
import openai
from typing import Dict, List
from backend.app.users.user import User, Level
from backend.db.mongo.mongo_connector import DBConnector
from backend.utils.decorators import timeit
from backend.db.sql.sql_connector import SQLConnector


class GPTClient:
    def __init__(
        self,
        user: User,
        db_connector: DBConnector,
    ):
        self.user = user
        self.db_connector = db_connector

    @property
    def metadata(self):
        return self._metadata()

    def _metadata(self):
        _metadata = self.db_connector.find({}, "metadata")['GPT_metadata']
        print(_metadata)
        return _metadata

    @property
    def level(self):
        user_level = self.user.level
        return Level.__members__[user_level].value["gpt"]

    def reinitialize_chat(self) -> None:
        """
        Re initialize the chat file by deleting it if there is already a
        conversation inside or by creating it if it does not exist
        """
        if self.user.previous_chats:
            self.user.previous_chats = None
            self.db_connector.update(
                {"username": self.user.username},
                {"previous_chat": self.user.previous_chats},
                "users",
            )
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
        print(template_text)
        return template_text

    def _api_key(self, config_file="./config/config.json"):
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

    # I want to add a new object to a collectio

    def store_chat(self, role: str, content: str) -> None:
        """
         Write a new answer or question into the chat json file
        Args:
            role (str):
            content (str):
        """
        # TODO: go back on this
        # self.db_connector.update({"username": self.user.username}, {"$addT"previous_chat": self.retrieve_chat()}, "users")
        #     self.formulate_message(role, content)
        #     f.write("\n")

    def retrieve_chat(self) -> List[Dict]:
        """
        Reads the chat json file and returns a json message  that is taken into argument by the model
        Returns: List[Dict]: List of messages to be processed by gpt api
        """
        with open(self.metadata.get("chat_file"), "r") as f:
            data = f.readlines()
        json_data = [json.loads(line.strip()) for line in data]
        messages = []
        for obj in json_data:
            messages.append(obj)
        print(messages)
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
            messages=self.retrieve_chat(),
            n=1,
            **self.level
            # logit_bias = json file - Modify the likelihood of specified tokens appearing in the completion.
        )
        collected_messages = []
        # if streaming
        # for chunk in response:
        #     chunk_message = chunk["choices"][0]["delta"]
        #     collected_messages.append(chunk_message)
        # answer = "".join([m.get("content", "") for m in collected_messages])

        # if not streamng
        answer = response["choices"][0]["message"]["content"]
        print(answer)

        # Build the answer in a string format considering only the content of the message
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


if __name__ == "__main__":
    sql_connector = SQLConnector()
    user1 = User("Meir", sql_connector)
    gpt = GPTClient(
        user=user1,
    )
    openai.api_key = gpt.api_key
    gpt.reinitialize_chat()
    print(gpt.ask_gpt("Oui, quel est le role du renard?"))
