from abc import ABC, abstractmethod
import math
class Loan(ABC):
    interest_rate : float
    
    @abstractmethod
    def get_interest(self):
        pass

    def calculate_emi(self,loan_amt, tenure):
        rate = self.get_interest()/1200
        tenure = tenure * 12
        emi = ((rate*math.pow((1+rate),tenure))/((math.pow((1+rate),tenure))-1))*loan_amt
        return round(emi,2)
        
