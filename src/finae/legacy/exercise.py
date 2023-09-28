import functools
import inspect

import ray

_EXERCISES = []

def _register_exercise(function_or_class, options):
    if not inspect.isfunction(function_or_class):
        raise TypeError('not supported')

    _EXERCISES.append(function_or_class)

def exercise(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _register_exercise(args[0], {})
    assert len(args) == 0 and len(kwargs) > 0
    return functools.partial(_register_exercise, options=kwargs)


def run_all_exercises():
    ray.init()

    for func in _EXERCISES:
        func()