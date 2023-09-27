import functools
from collections import defaultdict

from .llm import ask_llm

_CONCEPTS = []


def _finae_text(self):
    return self.text


def _finae_score(self):
    return self.score


def _finae_consistent(self):
    return self.score >= 0.9


def _finae_parse(self, text):
    self.text = text

    score_upper_bound = 0
    total_score = 0
    for method in dir(self):
        if method.startswith('__') or method.endswith('__'):
            continue
        m = getattr(self, method)
        if not hasattr(m, '__finae_weight_base_val__'):
            continue
        score_upper_bound = score_upper_bound + m.__finae_weight_base_val__

        ret_val = m()
        if ret_val is None:
            if getattr(m, '__finae_required__') is True:
                total_score = 0
                break
        else:
            total_score = total_score + m.__finae_weight_base_val__

    if not score_upper_bound:
        self.score = 0
    else:
        self.score = total_score / score_upper_bound


@classmethod
def _query_llm(cls, prompt):
    """Query instances for the given Concept class."""
    output = ask_llm(prompt)
    lines = output.split('\n')
    results = []
    for line in lines:
        c = cls()
        c.__finae_parse__(line)
        if c.__finae_consistent__():
            results.append(c)
    return results


def Concept(cls):

    # Public methods
    setattr(cls, 'query_llm', _query_llm)

    # Private methods
    setattr(cls, '__finae_text__', _finae_text)
    setattr(cls, '__finae_score__', _finae_score)
    setattr(cls, '__finae_consistent__', _finae_consistent)
    setattr(cls, '__finae_parse__', _finae_parse)
    _CONCEPTS.append(cls)
    return cls


def Attribute(method=None, **kwargs):
    def _harness(method):
        @functools.wraps(method)
        def _wrapper(self, *args, **kwargs):
            if not hasattr(self, '__finae_method_cache__'):
                setattr(self, '__finae_method_cache__', defaultdict(dict))

            if method.__name__ in self.__finae_method_cache__:
                return self.__finae_method_cache__[method.__name__]['val']
            ret_val = None
            try:
                ret_val = method(self, *args, **kwargs)
            except Exception as e:
                self.__finae_method_cache__[method.__name__]['exception'] = e
                ret_val = None
            self.__finae_method_cache__[method.__name__]['val'] = ret_val
            return ret_val

        setattr(_wrapper, '__finae_weight_base_val__',
                kwargs.get('weight', 1.0))
        setattr(_wrapper, '__finae_required__', kwargs.get('required', False))
        return _wrapper

    if method is None:
        return _harness
    else:
        return _harness(method)
