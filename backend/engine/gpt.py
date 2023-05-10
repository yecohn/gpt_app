import json
import time
import openai
from typing import Dict, List
from backend.app.users.user import UserInfo
from backend.db.mongo.mongo_connector import MongoConnector
from backend.utils.decorators import timeit
from backend.db.sql.sql_connector import SQLConnector


class GPTClient:
    def __init__(
        self,
        user: UserInfo,
        db_connector: MongoConnector,
    ):
        self.user = user
        self.db_connector = db_connector

    @property
    def metadata(self):
        return self._metadata()

    def _metadata(self):
        _metadata = self.db_connector.find({}, "metadata")["GPT_metadata"]
        print(_metadata)
        return _metadata

    @property
    def level(self):
        user_level = self.user.level
        return self.db_connector.find({"level": user_level}, "levels")["gpt"]

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

    @property
    def initial_prompt(self):
        with open("./data/starting_beginner_prompt_template.txt", "r") as file:
            return file.read()

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

        def replace_role(role: str) -> str:
            if role == "ai":
                return "system"
            elif isinstance(role, str):
                return "user"

        chat = self.db_connector.find({"user_id": self.user.id}, "chats")
        messages = chat["messages"]
        messages_gpt = [
            {"role": replace_role(m["user"]["name"]), "content": m["text"]}
            for m in messages
        ]
        return messages_gpt

    def create_lesson(self, lesson_prompt) -> str:
        messages = self.retrieve_chat().append(json.loads((lesson_prompt).strip()))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=1,
            **self.level
            # logit_bias = json file - Modify the likelihood of specified tokens appearing in the completion.
        )
        answer = response["choices"][0]["message"]["content"]
        return answer

    def ask_gpt_about_topic(self, transcript, topic_prompt) -> dict:
        messages = self.retrieve_chat()
        question = topic_prompt + "\n" + transcript
        question = self.formulate_message(role="user", content=question)
        messages += [question]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=1,
            **self.level
            # logit_bias = json file - Modify the likelihood of specified tokens appearing in the completion.
        )
        answer = response["choices"][0]["message"]["content"]
        return answer

    @timeit
    def ask_gpt(self, question) -> str:
        """ask gpt a question and get an answer
        Args:
            question (str): question to be asked

        Returns:
            str: answer to the question
        """
        question_gpt = {"role": "user", "content": question}
        chat = self.retrieve_chat()
        inital_prompt = {"role": "user", "content": self.initial_prompt}
        chat.insert(0, inital_prompt)
        chat.append(question_gpt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=chat, n=1, **self.level
        )
        answer = response["choices"][0]["message"]["content"]
        print(answer)

        # Build the answer in a string format considering only the content of the message
        # self.store_chat("system", answer)
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
