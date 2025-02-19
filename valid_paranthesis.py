from abc import ABC, abstractmethod

class BracketService(ABC):
    
    @abstractmethod
    def is_valid_open():
        pass

    @abstractmethod
    def is_valid_close():
        pass

    @abstractmethod
    def get_open_bracket():
        pass


class RegularBracketService(BracketService):
    def __init__(self):
        self.mapping = {} 
        self.open_braces = set()

    def add_pair(self,open, close):
        self.open_braces.add(open)
        self.mapping[close] = open

    def is_valid_open(self, ch):
        return ch in self.open_braces
    
    def is_valid_close(self, ch):
        return ch in self.mapping
    
    def get_open_bracket(self, ch):
        return self.mapping[ch]
    
def console_output(func):
    def wrapper(*args):
        ans = func(*args)
        if ans:
            print(f"{args[1]} is valid paranthesis")
        else:
            print(f"{args[1]} is invalid paranthesis")
    return wrapper


class ParanthesisChecker:
    def __init__(self, bracket_service : BracketService):
        self._stack = []
        self.bracket_service = bracket_service
        

    def clear(self):
        self._stack = []

    @console_output
    def validate(self, test_string):
        if len(test_string) % 2 != 0:
            return False
        
        for char in test_string:
            if self.bracket_service.is_valid_open(char):
                self._stack.append(char)

            elif (not self._stack) or \
            (not self.bracket_service.is_valid_close(char)) or \
            (self.bracket_service.get_open_bracket(char) != self._stack[-1]):
                return False
            else:
                self._stack.pop()
        
        return len(self._stack) == 0
    
    

    
    

if __name__ == "__main__":
    bracket_service = RegularBracketService()
    bracket_service.add_pair("{","}")
    bracket_service.add_pair("(", ")")
    bracket_service.add_pair("[","]")
    bracket_service.add_pair("0","1")

    checker = ParanthesisChecker(bracket_service)

    test_cases = [
        "((])",
        "",
        "(0()1)",
        "{[()]}",
        "{0)}",
        "0101012",
        "(01)"
    ]

    for test in test_cases:
        checker.clear()
        checker.validate(test)

    


    


