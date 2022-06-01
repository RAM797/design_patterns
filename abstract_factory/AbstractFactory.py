from abc import ABCMeta, abstractmethod
class AbstractFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_bank(self):
        pass

    @abstractmethod
    def get_loan(self):
        pass

