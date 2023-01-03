class Car:
    def __init__(self):
        self.company = 'Dodge'
        self.model = 'charger'
        self.color = 'red'
    def __str__(self):
        return str(self.__dict__)