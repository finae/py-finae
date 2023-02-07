import functools
import inspect

import ray


def init():
    ray.init()


def _register_func_or_class(function_or_class, options):
    if inspect.isfunction(function_or_class):
        @ray.remote
        def _finae_remote_wrapper(*args, **kwargs):
            print(f'_finae_remote_wrapper = {args}')
            return function_or_class(*args, **kwargs)

        @functools.wraps(function_or_class)
        def _function_proxy(*args, **kwargs):
            print('_function_proxy')
            t = _finae_remote_wrapper.remote(*args, **kwargs)
            return ray.get(t)

        return _function_proxy

    if inspect.isclass(function_or_class):
        raise TypeError('TODO')

    raise TypeError('not supported')


def learn(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _register_func_or_class(args[0], {})
    assert len(args) == 0 and len(kwargs) > 0
    return functools.partial(_register_func_or_class, options=kwargs)
