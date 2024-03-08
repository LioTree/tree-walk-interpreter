from callable_ import Callable_
import time

class Clock(Callable_):
    def arity(self):
        return 0

    def call(self,interpreter,arguments):
        return time.time()

    def __str__(self):
        return '<native fn>'

if __name__=='__main__':
    clock = Clock()
    print(isinstance(clock,Callable_))