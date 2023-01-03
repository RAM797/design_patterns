class Car:
    def __init__(self):
        self.engine = None
        self.tires = None
        self.seating = None

    def __str__(self):
        return str(self.__dict__)