import imp
from AbstractFactory import AbstractFactory
from HomeLoan import HomeLoan
from Ed_loan import EdLoan
class LoanFactory(AbstractFactory):
   def get_loan(self,loan_type,ir):
       if loan_type.upper() == 'EDUCATION':
           return EdLoan(ir)
       elif loan_type.upper() == 'HOME':
           return HomeLoan(ir)
   def get_bank(self):
        return None

    



