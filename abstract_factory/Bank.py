from abc import ABC, abstractmethod
class Bank(ABC):
    @abstractmethod
    def get_interest():
        pass