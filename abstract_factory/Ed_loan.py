from Loan import Loan
class EdLoan(Loan):

    def __init__(self,ir):
        Loan.interest_rate =ir

    def get_interest(self):
        return Loan.interest_rate

    