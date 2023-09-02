import os

os.environ['OPENAI_API_BASE'] = "https://shale.live/v1"
os.environ['OPENAI_API_KEY'] = "shale-/vOlxxgbDAD7f5"

from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9, max_tokens=2048)

prompt = "List top mountains in the world"
result = llm(prompt)
print(result)

