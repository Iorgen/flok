from abc import ABCMeta

class A:
    def __init__(self):
        print('A')


class B(A):
    def __init__(self):
        super().__init__()
        print('B')


if __name__ == '__main__':
    b = B()
    print(isinstance(b, A))

