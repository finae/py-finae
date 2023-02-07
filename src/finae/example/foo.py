import finae

finae.init()


@finae.learn
def foo(name):
    print(f'im {name}')


if __name__ == '__main__':
    foo('fol')
