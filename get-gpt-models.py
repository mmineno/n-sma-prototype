# import openai
# import os
# import dotenv
# import requests

# # OpenAIのAPIキーを設定します
# dotenv.load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# url = "https://api.openai.com/v1/models"
# headers = {"Authorization": f"Bearer {openai.api_key}"}

# response = requests.get(url, headers=headers)
# models = response.json()

# for model in models["data"]:
#     print(model["id"])
# print(len(model))
