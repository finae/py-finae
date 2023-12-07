import functools
import inspect
import os
import pickle
import pprint
import random
import uuid
from collections import Counter

from .llm import ask_llm

_CONCEPTS_REGISTRY = []


def _most_frequent(input_list):
    occurence_count = Counter(input_list)
    return occurence_count.most_common(1)[0][0]


def _line_by_line_parser(llm_output, concepts):
    lines = llm_output.split('\n')
    results = []
    # Basic line-by-line parser.
    for line in lines:
        for cls in concepts:
            c = cls(line)
            if c.consistent():
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
        self._concepts = [
            c for c in concepts if hasattr(c, '__finae_debug__')]

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


class Budget:
    def __init__(self, num_of_attributes=None):
        self._num_of_attributes = num_of_attributes
        self._remain = 70 * num_of_attributes
        
    def remain(self):
        return self._remain

    def spend(self, cost):
        self._remain = self._remain - cost
        
    def split(self):
        return 


def _constructor(self, text, budget=None):
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
            'produced': dict(),
        }
        if budget is None:
            all_attributes = self.__finae_all_attributes__()
            self.budget = Budget(num_of_attributes=len(all_attributes))
        self.invest(budget=self.budget)
        if self.consistent():
            db.insert(self.__finae_data__)


def _finae_id(self):
    return self.__finae_data__['id']


def _finae_text(self):
    return self.__finae_data__['text']


def _finae_score(self):
    return self.__finae_data__['score']


def _finae_produce(self, key, value):
    """Produce hook"""
    if key not in self.produced():
        self.produced()[key] = list()
    self.produced()[key].append(value)


def _finae_produced(self):
    return self.__finae_data__['produced']


def _finae_get(self, key):
    if key not in self.produced():
        raise KeyError
    most = _most_frequent(self.produced()[key])
    return most


def _finae_consistent(self):
    for key, value in self.produced().items():
        if (not value) or (not isinstance(value, list)):
            return False
    return True


@classmethod
def _finae_all_attributes(cls):
    attributes = []
    for method in dir(cls):
        if method.startswith('__') or method.endswith('__'):
            continue
        m = getattr(cls, method)
        if not hasattr(m, '__finae_attribute_price__'):
            continue
        attributes.append(method)
    return attributes


def _finae_invest(self, budget):
    all_attributes = self.__finae_all_attributes__()
    
    while budget > 0:
        method = random.choice(all_attributes)
        m = getattr(self, method)
        price = m.__finae_attribute_price__
        key = m.__finae_attribute_key__
        
        spend = budget / len(all_attributes)

        # TODO: May return a Product dataclass instead
        cost = m(budget=spend, price=price, key=key, produce=self.produce)
        budget = budget - cost
            
        


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
    setattr(cls, 'query', _query_llm)
    setattr(cls, 'id', _finae_id)
    setattr(cls, 'text', _finae_text)
    setattr(cls, 'score', _finae_score)
    setattr(cls, 'produce', _finae_produce)
    setattr(cls, 'produced', _finae_produced)
    setattr(cls, 'get', _finae_get)
    setattr(cls, 'consistent', _finae_consistent)
    setattr(cls, 'invest', _finae_invest)
    setattr(cls, '__finae_all_attributes__', _finae_all_attributes)
    setattr(cls, '__finae_database__', _ConceptDatabase(cls))
    setattr(cls, '__finae_debug__', _finae_debug)

    _CONCEPTS_REGISTRY.append(cls)
    return cls


def Attribute(method=None, **kwargs):
    def _harness(method):
        @functools.wraps(method)
        def _wrapper(self, *args, **kwargs):
            
            # Deduct method base price
            budget = kwargs['budget']
            price = kwargs['price']
            budget = budget - price
            if budget <= 0:
                return None, kwargs['budget']
            kwargs['budget'] = budget

            ret_val = None
            try:
                ret_val = method(self, *args, **kwargs)
            except Exception as e:
                ret_val = None
            return ret_val

        setattr(_wrapper, '__finae_attribute_weight_base_val__',
                kwargs.get('weight', 1.0))
        setattr(_wrapper, '__finae_attribute_required__',
                kwargs.get('required', False))
        setattr(_wrapper, '__finae_attribute_price__',
                kwargs.get('price', 1.0))
        setattr(_wrapper, '__finae_attribute_key__',
                kwargs.get('key', method.__name__))
        return _wrapper

    if method is None:
        return _harness
    else:
        return _harness(method)
