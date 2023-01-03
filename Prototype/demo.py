from car import Car
from prototype import Prototype

dodge = Car()
print(dodge)
prototype = Prototype()
prototype.register_car('dodge', dodge)
dodge_clone = prototype.clone_car('dodge', color = 'green')
print(dodge_clone)