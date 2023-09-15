from functools import cache

_CONCEPTS = []


def _score(self):
    print('score')


def Concept(cls):
    setattr(cls, '__finae_score__', _score)
    print(dir(cls))
    return cls


def Attribute(method):
    method = cache(method)
    print(dir(method))
    return method
