import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
job = openai.FineTuningJob.create(
    training_file=os.getenv("OPENAI_FILE_ID"), 
    model="gpt-3.5-turbo",
    hyperparameters={"n_epochs":10}
)
print(job)