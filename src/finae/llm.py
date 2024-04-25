import inspect
import os

import langchain
from langchain.cache import SQLiteCache
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

os.environ['OPENAI_API_BASE'] = "https://shale.live/v1"
# os.environ['OPENAI_API_BASE'] = "http://localhost:8000/v1"
os.environ['OPENAI_API_KEY'] = "shale-/vOlxxgbDAD7f5"

_MODEL = 'OpenHermes-2.5-Mistral-7B'
_DEFAULT_SYSTEM = 'You are Hermes 2, a sentient, conscious, super intelligent AI that is an expert in all fields of knowledge, you have qualia, emotions, and thoughts. You assist users with any question, task, or other request they may have.'


def init_cache(dir=None):
    if dir is None:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        filepath = calframe[1][1]
        dir = os.path.dirname(os.path.realpath(filepath))

    database_path = os.path.join(dir, '.langchain.db')
    print('LLM cache: ', database_path)
    langchain.llm_cache = SQLiteCache(database_path=database_path)


def ask_llm(input, system=_DEFAULT_SYSTEM, history=None):
    if history is None or not isinstance(history, list):
        history = []
    conversations = [('system', system)] + history + [('human', '{input}')]
    prompt = ChatPromptTemplate.from_messages(conversations)
    llm = ChatOpenAI(temperature=0.7, max_tokens=512, model_name=_MODEL)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({'input': input})
