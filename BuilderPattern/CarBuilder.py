from abc import ABC, abstractmethod
class CarBuilder(ABC):

    @abstractmethod
    def build_engine(self):
        pass

    @abstractmethod
    def build_tires(self):
        pass

    @abstractmethod
    def build_seating(self):
        pass

    @abstractmethod
    def get_car(self):
        pass

    def construct_car(self):
        self.build_engine()
        self.build_tires()
        self.build_seating()
    