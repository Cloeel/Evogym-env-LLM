import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
job = openai.FineTuningJob.create(
    training_file="file-abc123", 
    model="gpt-3.5-turbo"
)
print(job)