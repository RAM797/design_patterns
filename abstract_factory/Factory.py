from BankFactory import BankFactory
from LoanFactory import LoanFactory
class FactoryCreator():
    def create_factory(fact_type: str):
        if fact_type.upper() == 'BANK':
            return BankFactory()
        elif fact_type.upper() == 'LOAN':
            return LoanFactory()

