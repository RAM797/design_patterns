from CarBuilder import CarBuilder
from car import Car

class SeltosBuilder(CarBuilder):
    
    def __init__(self):
        self.car = Car()

    def build_engine(self):
        self.car.engine = "Petrol1.5"
    
    def build_seating(self):
        self.car.seating=5

    def build_tires(self):
        self.car.tires = "apollo"

    def get_car(self):
        return self.car


    