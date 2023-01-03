from car import Car
import copy
class Prototype:
    def __init__(self):
        self.cars = {}

    def register_car(self, name, car: Car):
        self.cars[name] = car

    def deregister_car(self,name):
        del self.cars[name]

    def clone_car(self, name, **attr):
        clone = copy.deepcopy(self.cars[name])
        clone.__dict__.update(attr)
        return clone
