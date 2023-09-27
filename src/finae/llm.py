import os
import inspect

import langchain
from langchain.cache import SQLiteCache
from langchain.llms import OpenAI

os.environ['OPENAI_API_BASE'] = "https://shale.live/v1"
os.environ['OPENAI_API_KEY'] = "shale-/vOlxxgbDAD7f5"


def init_cache(dir=None):
    if dir is None:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        filepath = calframe[1][1]
        dir = os.path.dirname(os.path.realpath(filepath))

    database_path = os.path.join(dir, '.langchain.db')
    print('LLM cache: ', database_path)
    langchain.llm_cache = SQLiteCache(database_path=database_path)


def ask_llm(prompt):
    llm = OpenAI(temperature=0.9, max_tokens=2048)
    result = llm(prompt)
    return result


def query_concepts(prompt, *concepts):
    """Query instances for given Concepts from LLM."""
    finae_concepts = [c for c in concepts if hasattr(c, '__finae_parse__')]
    output = ask_llm(prompt)
    lines = output.split('\n')
    results = []
    for line in lines:
        for cls in finae_concepts:
            c = cls()
            c.__finae_parse__(line)
            if c.__finae_consistent__():
                results.append(c)
    return results