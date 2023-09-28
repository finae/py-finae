from .core import Attribute, Concept
from .legacy.exercise import exercise, run_all_exercises
from .legacy.learn import learn
from .llm import ask_llm, init_cache, query_concepts


def say_hello():
    print('hello')
