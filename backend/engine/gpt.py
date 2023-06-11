import json
import openai
from typing import List
from backend.app.users.user import UserInfo
from backend.db.mongo.mongo_connector import access_mongo, MongoConnector
from backend.utils.decorators import timeit
from backend.db.sql.sql_connector import SQLConnector, access_sql
from fastapi import Depends
from datetime import datetime




class GPTClient:
    def __init__(self):
        self.db_connector : MongoConnector = Depends(access_mongo)

    @property
    def metadata(self):
        return self._metadata()

    def _metadata(self):
        _metadata = self.db_connector.find({}, "metadata")["GPT_metadata"]
        print(_metadata)
        return _metadata

    @property
    def level(self):
        return self._level()
    
    def _level(self):
        return self.db_connector.find({}, "levels")["gpt"]

    @property
    def api_key(self):
        return self._api_key()
    
    def _api_key(self, config_file="./config/config.json"):
        with open(config_file, "r") as config:
            CONFIG = json.load(config)
        return CONFIG["openai_api_key"]

    def formulate_db_message(user_id: int, user_name: str, origin: str, text: str, date: datetime):
        message = {
            "user": {"id": user_id, "name": user_name},
            'origin': origin,
            "text": text,
            "createdAt": date,
        }
        return message

    def get_username(self, chatId: int) -> str:
        user = UserInfo(userid=chatId)
        return user.username

    def formulate_message(self, role: str, content: str) -> dict:
        return {"role": role, "content": content}

    def formulate_messages(self, messages: List[dict]) -> List[dict]:
        formatted_messages = [
            self.formulate_message(role=m['user']['name'], content=m['text']) 
            for m in messages
        ]
        return formatted_messages

    def query_gpt_api(self, messages: List[dict]) -> dict:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=1,
            **self.level
            # logit_bias = json file - Modify the likelihood of specified tokens appearing in the completion.
        )
        return response["choices"][0]["message"]["content"]
    
    # From chat router
    def load_chat(self, chatId: int) -> dict:
        return self.db_connector.find(query = {"chat_id": chatId}, collection = "chats")

    def answer(self, chatId: int, user_prompt: str) -> None:
        chat = self.load_chat(chatId = chatId)
        
        chat_messages = self.formulate_messages(chat["messages"])
        
        initial_prompt = self.formulate_message(role="user", content=str(chat["initial_prompt"]))
        chat_messages.insert(0, initial_prompt)
        
        prompt = self.formulate_message(role="user", content=str(prompt))
        chat_messages.append(prompt)

        answer = self.query_gpt_api(messages=chat_messages)
        question_json = self.formulate_db_message(
            user_id = chatId, 
            user_name = self.get_username(chatId), 
            origin = "user", 
            text = user_prompt, 
            date = datetime.now()
        )
        answer_json = self.formulate_db_message(
            user_id = chatId, 
            user_name = 'teaching assistant', 
            origin = 'system', 
            text = answer, 
            date = datetime.now()
        )
        self.db_connector.update_one(
            query={"chat_id": chatId},
            setter={"$push": {"messages": {"$each": [question_json, answer_json]}}},
            collection_name="chats",
        )

    def reset_chat(self, chatId: int) -> None:
        chat = self.load_chat(chatId = chatId)
        
        initial_prompt = self.formulate_message(role="user", content=str(chat["initial_prompt"]))
        answer = self.query_gpt_api(messages=initial_prompt)

        answer_json = self.formulate_db_message(
            user_id = chatId, 
            user_name = 'teaching assistant', 
            origin = 'system', 
            text = answer, 
            date = datetime.now()
        )
        self.db_connector.update_one(
            query={"chat_id": chatId},
            setter={"$set": {"messages": [answer_json]}},
            collection_name="chats",
        )



    # def start_new_chat(self, initial_prompt) -> dict:
    #     messages = self.formulate_message(role="user", content=initial_prompt)
    #     return self.query_gpt_api([messages])


    # def create_lesson(self, lesson_prompt) -> dict:
    #     messages = self.retrieve_chat()
    #     question = self.formulate_message(role="user", content=lesson_prompt)
    #     messages += [question]
    #     return self.query_gpt(messages)

    # def discuss_topic(self, topic_prompt) -> dict:
    #     messages = self.retrieve_chat()
    #     question = self.formulate_message(role="user", content=topic_prompt)
    #     messages += [question]
    #     return self.query_gpt(messages)


if __name__ == "__main__":
    sql_connector = SQLConnector()
    user1 = User("Meir", sql_connector)
    gpt = GPTClient(
        user=user1,
    )
    openai.api_key = gpt.api_key
    gpt.reinitialize_chat()



    # def reinitialize_chat(self) -> None:
    #     """
    #     Re initialize the chat file by deleting it if there is already a
    #     conversation inside or by creating it if it does not exist
    #     """
    #     if self.user.previous_chats:
    #         self.user.previous_chats = None
    #         self.db_connector.update(
    #             {"username": self.user.username},
    #             {"previous_chat": self.user.previous_chats},
    #             "users",
    #         )
    #     initial_prompt = self.initial_prompt
    #     self.store_chat(role="user", content=initial_prompt)

    # @property
    # def question(self) -> str:
    #     """load question from input file"""
    #     with open(self.metatadata.get("input_file"), "r") as f:
    #         question = f.read()
    #     return question

    # @question.setter
    # def question(self, question):
    #     with open(self.metadata.get("input_file"), "w") as f:
    #         f.write(question)

    # @property
    # def answer(self) -> str:
    #     with open(self.metadata.get("output_file"), "r") as f:
    #         answer = f.read()
    #     return answer

    # @answer.setter
    # def answer(self, answer):
    #     with open(self.metadata.get("output_file"), "w") as f:
    #         f.write(answer)


    # def start_chat(self) -> None:
    #     """start conversation by submitting first question to gpt"""
    #     self.ask_gpt(question="")

    # def save_answer(self, answer: str) -> None:
    #     """save answer to file for later use"""
    #     with open(self.output_file, "w") as f:
    #         f.write(answer)