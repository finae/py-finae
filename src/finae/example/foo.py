import finae

@finae.learn
def foo(name):
    print(f'im {name}')
    return name


@finae.exercise
def test_foo():
    foo('foo')
    foo('fol')
    foo('bar')
    foo.__real__('real')


@finae.exercise
def test_debug():
    foo.debug_print_records()


if __name__ == '__main__':
    finae.run_all_exercises()
