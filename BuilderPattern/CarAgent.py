from CarBuilder import CarBuilder
class CarAgent:
    def __init__(self, builder: CarBuilder):
        self.builder = builder

    def build_car(self):
        self.builder.construct_car()

    def get_car(self):
        return self.builder.get_car()
        