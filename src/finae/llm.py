import os

import langchain
from langchain.cache import SQLiteCache
from langchain.llms import OpenAI

os.environ['OPENAI_API_BASE'] = "https://shale.live/v1"
os.environ['OPENAI_API_KEY'] = "shale-/vOlxxgbDAD7f5"


def init_cache(dir):
    langchain.llm_cache = SQLiteCache(database_path= os.path.join(dir, '.langchain.db'))


def ask_llm(prompt):
    llm = OpenAI(temperature=0.9, max_tokens=2048)
    result = llm(prompt)
    return result
