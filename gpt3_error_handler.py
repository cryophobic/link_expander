#This script is an error handler and suggestion module intended to speed the process of debugging and writing useful code
#It uses GPT-3.5 to parse errors and determine how to solve problems.

import os
import openai
from dotenv import load_dotenv

# This line loads the variables from the .env file
load_dotenv()

# The credentials are pulled from the .env
openai.organization = os.getenv("OPEN_AI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt3(error_description):
    prompt = f"An error occurred in my Python script: {error_description}. Can you provide a brief summary and a couple of possible solutions?"

    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()
