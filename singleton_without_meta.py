class Singleton:

    _instance = None
    _initialized = False
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
    
    def __init__(self, value):
        if not self.__class__._initialized:
            self.value = value
            self.__class__._initialized = True


a = Singleton(10)
b = Singleton(20)
a.value = 40
print(b.value)


    

        
    
