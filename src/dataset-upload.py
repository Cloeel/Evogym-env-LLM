import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.File.create(
  file=open("dataset/gpt3-5turbo-dataset-v4.jsonl", "rb"),
  purpose='fine-tune'
)
print(response)