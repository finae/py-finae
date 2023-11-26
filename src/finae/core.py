import functools
import inspect
import os
import pickle
import pprint
import uuid

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
    db = self.__finae_database__
    from_cache = db.retrieve_by_text(text)
    if from_cache:
        self.__finae_data__ = from_cache
    else:
        self.__finae_data__ = {
            'id': str(uuid.uuid4()),
            'text': text,
            'score': 0,
            'method_cache': dict(),
        }
        self.__finae_parse__()
        if self.__finae_consistent__():
            db.insert(self.__finae_data__)


def _finae_id(self):
    return self.__finae_data__['id']


def _finae_text(self):
    return self.__finae_data__['text']


def _finae_score(self):
    return self.__finae_data__['score']


def _finae_consistent(self):
    return self.__finae_score__() >= 1.0


@classmethod
def _finae_all_attributes(cls):
    attributes = []
    for method in dir(cls):
        if method.startswith('__') or method.endswith('__'):
            continue
        m = getattr(cls, method)
        if not hasattr(m, '__finae_attribute_weight_base_val__'):
            continue
        attributes.append(method)
    return attributes


def _finae_parse(self):
    total_weight = sum([getattr(self, method).__finae_attribute_weight_base_val__
                        for method in self.__finae_all_attributes__()])
    total_score = 0
    for method in self.__finae_all_attributes__():
        m = getattr(self, method)
        weight_base_val = m.__finae_attribute_weight_base_val__

        ret_val = m()
        if ret_val is None:
            if getattr(m, '__finae_attribute_required__') is True:
                total_score = 0
                break
        else:
            total_score = total_score + weight_base_val

    if not total_weight:
        normalized_score = 0
    else:
        normalized_score = total_score / total_weight

    self.__finae_data__['score'] = normalized_score


@classmethod
def _finae_debug(cls):
    db = cls.__finae_database__
    db.print()


@classmethod
def _query_llm(cls, prompt):
    """Simple extraction as example."""
    extraction = Extraction(prompt, [cls])
    results = extraction.extract(rounds=1)
    return results


class _ConceptDatabase:

    def __init__(self, given_cls):
        self._given_cls = given_cls
        self._filedb_path = self._get_filedb_path()

        # text -> datapoint
        self._dataframe = self._create_or_load_file_db()

    def _get_filedb_path(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        filepath = os.path.realpath(calframe[3][1])
        dirpath, filename = os.path.split(filepath)

        class_name = self._given_cls.__name__
        database_filepath = os.path.join(
            dirpath, f'{filename}.{class_name}.finae')
        return database_filepath

    def _create_dataframe(self):
        return dict()

    def _create_or_load_file_db(self):
        dataframe = None
        if os.path.exists(self._filedb_path):
            # TODO Database file SQLite.
            with open(self._filedb_path, 'rb') as f:
                dataframe = pickle.load(f)
        else:
            dataframe = self._create_dataframe()
        return dataframe

    def retrieve_by_text(self, text):
        return self._dataframe.get(text, None)

    def insert(self, datapoint):
        self._dataframe[datapoint['text']] = datapoint
        self.save()

    def save(self):
        with open(self._filedb_path, 'wb') as f:
            pickle.dump(self._dataframe, f, pickle.HIGHEST_PROTOCOL)

    def print(self):
        print(self._filedb_path)
        pprint.pprint(self._dataframe)


def Concept(cls):
    setattr(cls, '__init__', _constructor)
    setattr(cls, '__finae_query_llm__', _query_llm)
    setattr(cls, '__finae_id__', _finae_id)
    setattr(cls, '__finae_text__', _finae_text)
    setattr(cls, '__finae_score__', _finae_score)
    setattr(cls, '__finae_consistent__', _finae_consistent)
    setattr(cls, '__finae_parse__', _finae_parse)
    setattr(cls, '__finae_all_attributes__', _finae_all_attributes)
    setattr(cls, '__finae_database__', _ConceptDatabase(cls))
    setattr(cls, '__finae_debug__', _finae_debug)

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
