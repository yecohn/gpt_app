import json
from backend.utils import timeit
import time

import openai


class GPTClient:
    def __init__(
        self, input_file="../data/input.txt", output_file="../data/output.txt"
    ):
        self.input_file = input_file
        self.output_file = output_file
        with open(input_file, "r") as f:
            self.question = f.read()

        with open(output_file, "r") as f:
            self.answer = f.read()

    def _api_key(self, config_file="../config.json"):
        with open(config_file, "r") as config:
            CONFIG = json.load(config)
        return CONFIG["openai_api_key"]

    @property
    def api_key(self):
        return self._api_key()

    @timeit
    def ask_gpt(self, question) -> str:
        """ask gpt a question an return a string as answer

        Returns:
            str: answer from gpt
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": question},
            ],
        )
        answer = ""
        for choice in response.choices:
            answer += choice.message.content
        
        return answer

    def save_answer(self, answer) -> None:
        with open(self.output_file, "w") as f:
            f.write(answer)

    def run_agent(self):
        """run agent to run gpt request on entering"""

        while 1:
            self.ask_gpt()
            time.sleep(1)


if __name__ == "__main__":
    gpt = GPTClient()
    openai.api_key = gpt.api_key
    gpt.run_agent()
