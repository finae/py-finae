import functools
import inspect

import ray


def _register_func_or_class(function, options):
    if not inspect.isfunction(function):
        raise TypeError('not supported')
        
    @ray.remote
    def _finae_remote_wrapper(*args, **kwargs):
        print(f'_finae_remote_wrapper = {args}')
        return function(*args, **kwargs)

    class WrapperObject:

        def __init__(self, function, options):
            self._func = function
            self._options = options

        @functools.wraps(function)
        def __call__(self, *args, **kwargs):
            print('WrapperObject.__call__')
            t = _finae_remote_wrapper.remote(*args, **kwargs)
            return ray.get(t)

    return WrapperObject(function, options)



def learn(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _register_func_or_class(args[0], {})
    assert len(args) == 0 and len(kwargs) > 0
    return functools.partial(_register_func_or_class, options=kwargs)
