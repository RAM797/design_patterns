from Bank import Bank

class SBI(Bank):
    def __init__(self) -> None:
        self._name = "SBI"
        self.interest_rates = {'HOME': 6.4, 'EDUCATION' : 6.8}
    def get_interest(self,loan_type):
        return  self.interest_rates[loan_type.upper()]
    


    