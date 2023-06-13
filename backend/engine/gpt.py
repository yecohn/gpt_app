import json
import openai
from typing import List
from backend.app.users.user import UserInfo
from backend.db.mongo.mongo_connector import MongoConnector
from datetime import datetime
from backend.app.models import Userinf
from bson.objectid import ObjectId

class GPTClient:
    def __init__(self):
        self.db_connector = MongoConnector('speakit')
        openai.api_key = self.api_key

    @property
    def metadata(self):
        return self._metadata()

    def _metadata(self):
        _metadata = self.db_connector.find({}, "metadata")["GPT_metadata"]
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

    def formulate_db_message(self, user_name: str, origin: str, text: str):
        message = {
            "user": {
                "name": user_name
            },
            'origin': origin,
            "text": text,
            "createdAt": datetime.now(),
        }
        return message

    def get_username(self, chatId: str) -> str:
        # call to mongoDB to retrieve user_id in chat
        user_id = self.db_connector.find(
            query = {'_id': ObjectId(chatId)}, 
            collection_name = 'chats'
            )['user_id']
        return UserInfo().retrieve_username(user_id = user_id)

    def formulate_message(self, role: str, content: str) -> dict:
        return {"role": role, "content": content}

    def formulate_messages(self, messages: List[dict]) -> List[dict]:
        formatted_messages = [
            self.formulate_message(role=m['origin'], content=m['text']) 
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
    
    def concatenate_chat(self, chatId: str, prompt: str, prompt_role: str = None) -> None:
        chat = self.load_chat(chatId = chatId)
        
        chat_messages = self.formulate_messages(chat["messages"])
        
        initial_prompt = self.formulate_message(role="system", content=str(chat["initial_prompt"]))
        chat_messages.insert(0, initial_prompt)
        if prompt_role:
            prompt = self.formulate_message(role=prompt_role, content=str(prompt))
        else:
            prompt = self.formulate_message(role="user", content=str(prompt))
        chat_messages.append(prompt)
        return chat_messages

    def retrieve_chatId(self, user_id: str) -> str:
        return self.db_connector.find(
            query = {'user_id': user_id}, 
            collection_name = 'chats'
            )['_id']
    
    # From chat router
    def load_chat(self, chatId: str) -> dict:
        return self.db_connector.find(
            query = {'_id': ObjectId(chatId)}, 
            collection_name = 'chats'
            )

    def answer(self, chatId: str, user_prompt: str) -> None:

        chat_messages = self.concatenate_chat(chatId = chatId, prompt = user_prompt)
        answer = self.query_gpt_api(messages=chat_messages)
        question_json = self.formulate_db_message(
            user_name = self.get_username(chatId), 
            origin = 'user', 
            text = user_prompt, 
        )
        answer_json = self.formulate_db_message(
            user_name = 'teaching assistant', 
            origin = 'assistant', 
            text = answer, 
        )
        self.db_connector.update_one(
            query={'_id': ObjectId(chatId)},
            setter={"$push": {"messages": {"$each": [question_json, answer_json]}}},
            collection_name="chats",
        )

    def reset_chat(self, chatId: str) -> None:
        chat = self.load_chat(chatId = chatId)
        
        initial_prompt = self.formulate_message(role="system", content=str(chat["initial_prompt"]))
        answer = self.query_gpt_api(messages=[initial_prompt])

        answer_json = self.formulate_db_message(
            user_name = 'teaching assistant', 
            origin = 'assistant', 
            text = answer, 
        )
        self.db_connector.update_one(
            query={'_id': ObjectId(chatId)},
            setter={"$set": {"messages": [answer_json]}},
            collection_name="chats",
        )

    # From authentification router
    def initialize_new_chat(self, user_id: str, inf: Userinf) -> str:
        initial_prompt = self.metadata["initial_prompt_template"].copy()
        initial_prompt['native_language'] = inf.native
        initial_prompt['target_language'] = inf.target
        initial_prompt['user']['name'] = inf.username
        initial_prompt['user']['level'] = 'Beginner'
        initial_prompt['parameters']['level'] = 'Beginner'

        initial_prompt = self.formulate_message(role='system', content=str(initial_prompt))
        answer = self.query_gpt_api(messages=[initial_prompt])

        answer_json = self.formulate_db_message(
            user_name = 'teaching assistant', 
            origin = 'assistant', 
            text = answer 
        )

        chat = {
            'user_id': user_id,
            'messages': [answer_json],
            'initial_prompt': initial_prompt,
        }
        chatInsertionObject = self.db_connector.insert_one(chat, 'chats').inserted_id
        return str(chatInsertionObject)

    # From topic router
    def trigger_topic(self, chatId: str, topic_id: int) -> None:  
        

        topic_prompt = self.metadata["topic_prompt_template"].copy()
        transcript = self.db_connector.find(
            query={"topic_id": topic_id}, 
            collection_name="topics",
        )['transcript']
        topic_prompt['video_summary'] = transcript

        chat_messages = self.concatenate_chat(chatId = chatId, prompt = str(topic_prompt), prompt_role='system')

        answer = self.query_gpt_api(messages=chat_messages)
        question_json = self.formulate_db_message(
            user_name = 'system', 
            origin = 'system', 
            text = str(topic_prompt), 
        )
        answer_json = self.formulate_db_message(
            user_name = 'teaching assistant', 
            origin = 'assistant', 
            text = answer, 
        )
        self.db_connector.update_one(
            query={"_id": ObjectId(chatId)},
            setter={"$push": {"messages": {"$each": [question_json, answer_json]}}},
            collection_name="chats",
        )

    def generate_lesson(self, chatId: str) -> str:
        lesson_prompt = self.metadata["lesson_prompt_template"].copy()
        chat_messages = self.concatenate_chat(chatId = chatId, prompt = str(lesson_prompt), prompt_role='system')
        answer = self.query_gpt_api(messages=chat_messages)
        return answer

if __name__ == "__main__":
    gpt = GPTClient()
    openai.api_key = gpt.api_key