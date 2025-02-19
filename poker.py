"""
Entities
----------------
Card  1-10, A-B
Hand   5 cards
Rule   interface (pair, three of a kind, flush)
Game   evaluate the hand with best rule
"""
from abc import ABC,ABCMeta,abstractmethod
from collections import defaultdict
from enum import Enum


class RuleName(Enum):
    Pair = "PAIR"
    ThreeOfAKind = "THREE OF A KIND"
    Flush = "FLUSH"

class Card:
    def __init__(self, value, symbol):
        self.__value = value
        self.__symbol = symbol
    
    def get_value(self):
        return self.__value
    
    def get_symbol(self):
        return self.__symbol
    
    def __repr__(self):
        return f'{self.__value}-{self.__symbol}'

class Hand():
    def __init__(self, limit = 5):
        self.limit = limit
        self.size = 0 # can remove this and use len(self.__hand)
        self.__hand = [] # hold cards

    def get_card(self,index) -> Card:
        if index > self.size:
            raise ValueError("card doesn't exist, index out of bounds")
        return self.__hand[index]
    
    def add_card(self, card: Card):
        if self.size < self.limit:
            self.__hand.append(card)
            self.size += 1
        else:
            raise ValueError(f"Exceeding hand limit of {self.limit} cards")
        
    def __iter__(self):
        self.it = 0
        return self
    
    def __next__(self):
        if self.it == self.size:
            raise StopIteration
        self.it += 1
        return self.__hand[self.it-1]
    
    def __repr__(self):
        repr = ", ".join(str(card) for card in self.__hand)
        return repr


class SingletonMeta(ABCMeta):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


    

class IRule(ABC, metaclass = SingletonMeta):
    @abstractmethod
    def get_rule(self) -> RuleName:
        pass
    
    # checks whether rule is satisfied
    @abstractmethod
    def evaluate(self, hand: Hand) -> bool:
        pass
        

class Pair(IRule):
    def __init__(self):
        self.val_map = defaultdict(int)

    def get_rule(self):
        return RuleName.Pair
    
    def evaluate(self, hand: Hand):
        for card in hand:
            val =  card.get_value()
            self.val_map[val] += 1
            if self.val_map[val] >= 2:
                return True
        return False
    
class ThreeOfAKind(IRule):
    def __init__(self):
        self.val_map = defaultdict(int)

    def get_rule(self):
        return RuleName.ThreeOfAKind
    
    def evaluate(self, hand: Hand):
        for card in hand:
            val =  card.get_value()
            self.val_map[val] += 1
            if self.val_map[val] >= 3:
                return True
        return False
    
class Flush(IRule):
    def __init__(self):
        self.symbols = set()
    def get_rule(self):
        return RuleName.Flush

    def evaluate(self, hand: Hand):
        for card in hand:
            self.symbols.add(card.get_symbol())
        return len(self.symbols) == 1
    

class Game:
    def __init__(self, hand):
        self.__hand = hand
        self.rules : dict[IRule, int]

    # rank starts from 1
    def set_rules(self, rule_rank : dict[IRule, int]):
        self.rules = rule_rank

    # we will give lucky rule 0 rank
    def set_lucky_rule(self, rule):
        self.rules[rule] = 0

    def evaluate_hand(self):
        win_rule, win_rank = None, float('inf')
        for rule, rank in self.rules.items():
            if rule.evaluate(self.__hand) and rank < win_rank:
                win_rule = rule.get_rule()
                win_rank = rank
        if win_rule:
            print(f"{self.__hand} is {win_rule.value}")
        else:
            print(f"no winning rules exist for {self.__hand}")


if __name__ == "__main__":
    hand = Hand()
    hand.add_card(Card(10,'A'))
    hand.add_card(Card(7,'A'))
    hand.add_card(Card(6,'A')) #hypothetical
    hand.add_card(Card(6,'A'))
    hand.add_card(Card(6,'A'))
    game = Game(hand)
    game.set_rules({
        Flush(): 1,
        ThreeOfAKind(): 2,
        Pair(): 3,
    })
    # game.set_lucky_rule(Pair())
    game.evaluate_hand()

                
            


    


    




