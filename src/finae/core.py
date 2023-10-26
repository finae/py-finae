import uuid
import functools

from .llm import ask_llm

_CONCEPTS_REGISTRY = []


def _line_by_line_parser(llm_output, concepts):
    lines = llm_output.split('\n')
    results = []
    # Basic line-by-line parser.
    for line in lines:
        for cls in concepts:
            c = cls(line)
            if c.__finae_consistent__():
                results.append(c)
    return results


class Conversation:

    def __init__(self, input):
        self.id = str(uuid.uuid4()),
        self.input = input
        self.output = ask_llm(input)

    def __str__(self):
        return f'{self.input}\n--->\n{self.output}'

    def line_by_line_parse(self, concepts):
        return _line_by_line_parser(self.output, concepts)


class Extraction:
    """Multiple-round, same prompt concepts extraction.

    Be able to record history and replay the extraction.
    """

    def __init__(self, prompt, concepts):
        self._concepts = [c for c in concepts if hasattr(c, '__finae_parse__')]

        self.id = str(uuid.uuid4()),
        self.prompt = prompt
        self.conversations = []
        self.extracted_concepts = []

    def extract(self, rounds=1):
        print('=== Extraction prompt:\n', self.prompt)
        for i in range(rounds):
            print('=== Round #', i)
            c = Conversation(self.prompt)
            print(c)
            results = c.line_by_line_parse(self._concepts)
            print('=== Extracted ', len(results))
            self.extracted_concepts.extend(results)
        return self.extracted_concepts


def _constructor(self, text):
    """Text could be anything to be parse, prompts, serialized string etc."""
    self.__finae_data__ = {
        'id': str(uuid.uuid4()),
        'text': text,
        'score': 0,
        'method_cache': dict(),
    }
    self.__finae_parse__()


def _finae_id(self):
    return self.__finae_data__['id']


def _finae_text(self):
    return self.__finae_data__['text']


def _finae_score(self):
    return self.__finae_data__['score']


def _finae_consistent(self):
    return self.__finae_score__() >= 1.0


def _finae_parse(self):
    score_upper_bound = 0
    total_score = 0
    for method in dir(self):
        if method.startswith('__') or method.endswith('__'):
            continue
        m = getattr(self, method)
        if not hasattr(m, '__finae_attribute_weight_base_val__'):
            continue

        weight_base_val = m.__finae_attribute_weight_base_val__
        score_upper_bound = score_upper_bound + weight_base_val

        ret_val = m()
        if ret_val is None:
            if getattr(m, '__finae_attribute_required__') is True:
                total_score = 0
                break
        else:
            total_score = total_score + weight_base_val

    if not score_upper_bound:
        normalized_score = 0
    else:
        normalized_score = total_score / score_upper_bound

    self.__finae_data__['score'] = normalized_score


@classmethod
def _query_llm(cls, prompt):
    """Simple extraction as example."""
    extraction = Extraction(prompt, [cls])
    results = extraction.extract(rounds=1)
    return results


def Concept(cls):
    setattr(cls, '__init__', _constructor)
    setattr(cls, 'query_llm', _query_llm)
    setattr(cls, '__finae_id__', _finae_id)
    setattr(cls, '__finae_text__', _finae_text)
    setattr(cls, '__finae_score__', _finae_score)
    setattr(cls, '__finae_consistent__', _finae_consistent)
    setattr(cls, '__finae_parse__', _finae_parse)

    _CONCEPTS_REGISTRY.append(cls)
    return cls


def Attribute(method=None, **kwargs):
    def _harness(method):
        @functools.wraps(method)
        def _wrapper(self, *args, **kwargs):
            method_cache = self.__finae_data__['method_cache']
            if method.__name__ in method_cache:
                return method_cache[method.__name__]['val']
            else:
                method_cache[method.__name__] = dict()
            ret_val = None
            try:
                ret_val = method(self, *args, **kwargs)
            except Exception as e:
                method_cache[method.__name__]['exception'] = e
                ret_val = None
            method_cache[method.__name__]['val'] = ret_val
            return ret_val

        setattr(_wrapper, '__finae_attribute_weight_base_val__',
                kwargs.get('weight', 1.0))
        setattr(_wrapper, '__finae_attribute_required__',
                kwargs.get('required', False))
        return _wrapper

    if method is None:
        return _harness
    else:
        return _harness(method)
