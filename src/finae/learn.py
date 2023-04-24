import functools
import inspect

from collections import deque

import ray


def _register_func_or_class(function, options):
    if not inspect.isfunction(function):
        raise TypeError('not supported')

    @ray.remote
    def _finae_remote_wrapper(*args, **kwargs):
        print(f'_finae_remote_wrapper = {args}')
        return function(*args, **kwargs)

    class WrapperObject:
        _MAX_RECORD = 5

        def __init__(self, function, options):
            self._func = function
            self._signature = inspect.signature(function)
            self._options = options
            self._args_recorder = deque()

        def _record_args(self, input, output):
            self._args_recorder.append((input, output))
            if len(self._args_recorder) > WrapperObject._MAX_RECORD:
                self._args_recorder.popleft()

        def debug_print_records(self):
            print(f'{function.__name__} {self._signature}')
            for r in self._args_recorder:
                print('  ' + str(r))

        @functools.wraps(function)
        def __remote__(self, *args, **kwargs):
            t = _finae_remote_wrapper.remote(*args, **kwargs)
            return ray.get(t)

        @functools.wraps(function)
        def __real__(self, *args, **kwargs):
            self._func(*args, **kwargs)

        @functools.wraps(function)
        def __call__(self, *args, **kwargs):
            input = (args, kwargs)
            output = self.__remote__(*args, **kwargs)
            self._record_args(input, output)

    return WrapperObject(function, options)

def learn(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _register_func_or_class(args[0], {})
    assert len(args) == 0 and len(kwargs) > 0
    return functools.partial(_register_func_or_class, options=kwargs)
