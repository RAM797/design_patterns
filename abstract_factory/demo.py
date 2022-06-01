from FactoryCreator import FactoryCreator

def main():
    bank_name = input("enter the name of bank\n")
    loan_type = input("enter the loan type\n")
    loan_amt = float(input("enter the loan amount\n"))
    loan_tenure = float(input("number of years\n"))
    bank_factory = FactoryCreator.get_factory("BANK")
    bank = bank_factory.get_bank(bank_name)
    loan_factory = FactoryCreator.get_factory("LOAN")
    ir = bank.get_interest(loan_type)
    loan = loan_factory.get_loan(loan_type, ir)
    print("your emi is: ",end=" ")
    print(loan.calculate_emi(loan_amt, loan_tenure))


    
    
if __name__ == '__main__':
    main()