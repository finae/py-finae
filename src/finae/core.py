from functools import cache

_CONCEPTS = []


def _finae_text(self):
    return self.text


def _finae_score(self):
    return self.score


def _finae_consistent(self):
    return self.score == 1.0


def _finae_parse(self, text):
    self.text = text

    score_upper_bound = 0
    total_score = 0
    for method in dir(self):
        if method.startswith('__') or method.endswith('__'):
            continue
        m = getattr(self, method)
        if not hasattr(m, '__finae_score_base_val__'):
            continue
        score_upper_bound = score_upper_bound + m.__finae_score_base_val__
        try:
            m()
            total_score = total_score + m.__finae_score_base_val__
        except:
            pass
    if not score_upper_bound:
        self.score = 0
    else:
        self.score = total_score / score_upper_bound


def Concept(cls):
    setattr(cls, '__finae_text__', _finae_text)
    setattr(cls, '__finae_score__', _finae_score)
    setattr(cls, '__finae_consistent__', _finae_consistent)
    setattr(cls, '__finae_parse__', _finae_parse)
    _CONCEPTS.append(cls)
    return cls


def Attribute(method, score=1.0):
    method = cache(method)
    setattr(method, '__finae_score_base_val__', score)
    return method
