from abc import ABCMeta, abstractmethod

class Callable_(metaclass=ABCMeta):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self,interpreter,arugments):
        pass