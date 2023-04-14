import openai
import time

openai.api_key = "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"

with open("input.txt", "r") as f:
    question = f.read()


while 1:
    with open("input.txt", "r") as f:
        new_question = f.read()
    if new_question != question:
        start = time.time()
        question  = new_question
        print("new question entered")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": question},
            ],
        )

        result = ""
        for choice in response.choices:
            result += choice.message.content

        end = time.time()
        print(result)
        print(f"inference time: {end - start}")
        with open("output.txt", "w") as f:
            f.write(result)
    else:
        print("no new question")
    time.sleep(1)
