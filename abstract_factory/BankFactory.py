from AbstractFactory import AbstractFactory
from HDFC import HDFC
from SBI import SBI
class BankFactory(AbstractFactory):

    def get_bank(self,b_name):

        if b_name.upper() == 'HDFC':
            return HDFC()
        elif b_name.upper() == 'SBI':
            return SBI()
        return None

    def get_loan(self):
        return None
        
    



