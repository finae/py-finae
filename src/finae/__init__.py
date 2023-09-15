from .core import Attribute, Concept
from .exercise import exercise, run_all_exercises
from .learn import learn
from .llm import ask_llm, init_cache, query_llm


def say_hello():
    print('hello')
