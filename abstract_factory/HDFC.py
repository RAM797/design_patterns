from Bank import Bank

class HDFC(Bank):
    def __init__(self) -> None:
        self._name = "HDFC"
        self.interest_rates = {'HOME': 6.8, 'EDUCATION' : 7}

    def get_interest(self,loan_type: str):
        return  self.interest_rates[loan_type.upper()]

    