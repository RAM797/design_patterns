class SigletonMeta(type):
    _instances = {}
    def __call__(cls, *args):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args)
        return cls._instances[cls]


class Singleton(metaclass=SigletonMeta):
    _initialized = False

    def __init__(self,value):
        if not self.__class__._initialized:
            self.value = value
            self.__class__._initialized = True


class Singleton2(metaclass=SigletonMeta):
    _initialized = False

    def __init__(self,value):
        if not self.__class__._initialized:
            self.ovalue = value
            self.__class__._initialized = True


a = Singleton(10)
b = Singleton(20)
x = Singleton2(50)
y = Singleton2(60)
a.value = 40
print(x==y, b.value)