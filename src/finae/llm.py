from langchain.llms import OpenAI
import os

os.environ['OPENAI_API_BASE'] = "https://shale.live/v1"
os.environ['OPENAI_API_KEY'] = "shale-/vOlxxgbDAD7f5"


def query(prompt):
    llm = OpenAI(temperature=0.9, max_tokens=2048)
    result = llm(prompt)
    return result
