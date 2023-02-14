import finae

@finae.learn
def foo(name):
    print(f'im {name}')


@finae.exercise
def test_foo():
    foo('foo')
    foo('fol')
    foo('bar')


if __name__ == '__main__':
    finae.run_all_exercises()
