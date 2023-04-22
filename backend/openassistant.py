import requests

API_URL = (
    "https://api-inference.huggingface.co/models/merve/chatgpt-prompt-generator-v12"
)
headers = {"Authorization": "Bearer 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 "}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def ask_openassistant(question):
    output = query(
        {
            "inputs": question,
        }
    )
    return output


output = ask_openassistant("Comment puis-je apprendre le francais ?")
print(output)
