import random 

class Bank:
    def __init__(self, bank_name, bank_balance, highest_withdrawal_amount, lowest_withdrawal_amount, lowest_deposit_amount):
        self.bank_name = bank_name
        self.__bank_balance = bank_balance
        self.users = {}  
        self.__total_loan_amount = 0
        self.loan_feature_enable = True
        self.highest_withdrawal_amount = highest_withdrawal_amount
        self.lowest_withdrawal_amount = lowest_withdrawal_amount
        self.lowest_deposit_amount = lowest_deposit_amount

    @property
    def bank_balance(self):
        return self.__bank_balance

    @bank_balance.setter
    def bank_balance(self, value):
        self.__bank_balance = value
        
    @property
    def total_loan_amount(self):
        return self.__total_loan_amount
    
    @total_loan_amount.setter
    def total_loan_amount(self, value):
        self.__total_loan_amount = value

    def create_account(self, name, email, address, account_type):
        account_number = random.randint(100000, 999999)
        while account_number in self.users:
            account_number = random.randint(100000, 999999)
        self.users[account_number] = {
            'name': name,
            'email': email,
            'address': address,
            'account_type': account_type,
            'balance': 0,
            'transactions': [],
            'loan_taken': 0,
            'loan_count': 0
        }
        self.bank_balance += self.lowest_deposit_amount  # Update bank balance
        print(f"\t\t\t||---------|| Congratulations! You have created successfully with account number: {account_number}    ||---------||")
        return account_number

    def delete_account(self, account_number):
        if account_number in self.users:
            self.bank_balance -= self.users[account_number]['balance']  # Update bank balance
            del self.users[account_number]
            print("\t\t\t||---------||  Account deleted successfully.   ||---------||")
        else:
            print("\t\t\t||---------||  Account does not exist  ||---------||")

    def show_all_accounts(self):
        for account_number, user_info in self.users.items():
            print(f"\t\t\t||---------||    Account Number: {account_number}   ||---------||")
            for key, value in user_info.items():
                print(key.capitalize() + ":", value)
            print("")

    def check_balance(self, account_number):
        if account_number in self.users:
            print(f"\t\t\t||---------||  Available Balance:  {self.users[account_number]['balance']}    ||---------||")
        else:
            print('\t\t\t||---------||  Account does not exist  ||---------||')

    def deposit(self, account_number, amount):
        if account_number in self.users:
            if amount >= self.lowest_deposit_amount:
                self.users[account_number]['balance'] += amount
                self.users[account_number]['transactions'].append(f"Deposited {amount}")
                self.bank_balance += amount
                print("\t\t\t||---------||  Deposit successful. ||---------||")
            else:
                print(f"\t\t||-----||  Sorry, we cannot deposit your amount because the minimum deposit amount is: {self.lowest_deposit_amount}  ||-----||")
        else:
            print("\t\t\t||------||  Account does not exist.  ||---------||")

    def withdraw(self, account_number, amount):
        if account_number in self.users:
            if self.users[account_number]['balance'] >= amount:
                if self.lowest_withdrawal_amount <= amount <= self.highest_withdrawal_amount:
                    self.users[account_number]['balance'] -= amount
                    self.bank_balance -= amount
                    self.users[account_number]['transactions'].append(f'Withdraw {amount}')
                    print("\t\t\t||---------||  Withdrawal successful. ||---------||")
                else:
                    print(f"\t\t\t||-------||   Amount should be between {self.lowest_withdrawal_amount} and {self.highest_withdrawal_amount}   ||-------||")
            else:
                print("\t\t\t||---------||Insufficient bank balance. ||---------||")
        else:
            print("\t\t\t||---------||  Account does not exist.   ||-------||")

    def transfer_money(self, from_account_number, to_account_number, amount):
        if from_account_number in self.users and to_account_number in self.users:
            if self.users[from_account_number]['balance'] >= amount:
                self.users[from_account_number]['balance'] -= amount
                self.users[to_account_number]['balance'] += amount
                self.users[from_account_number]['transactions'].append(f'Transfer {amount} to {to_account_number}')
                self.users[to_account_number]['transactions'].append(f"Received {amount} from {from_account_number}")
                print("\t\t\t||---------||  Transfer successful.    ||---------||")
            else:
                print("\t\t\t||---------||  Insufficient balance. ||---------||")
        else:
            print("\t\t\t||---------||  Account does not exist. ||---------||")

    def take_loan(self, account_number, loan_amount):

        if self.loan_feature_enable == True:
            if account_number in self.users:
                if self.users[account_number]['loan_count'] < 2:
                    self.users[account_number]['loan_taken'] += loan_amount
                    self.users[account_number]['balance'] += loan_amount
                    self.users[account_number]['transactions'].append(f'Took loan of {loan_amount}')
                    self.total_loan_amount += loan_amount
                    self.users[account_number]['loan_count'] += 1
                    print("\t\t\t\t\t\t||---------||    Loan taken successfully.    ||---------||")
                else:
                    print("\t\t\t||---------||  You have already taken the maximum number of loans. ||---------||")
            else:
                print("\t\t\t||---------|| Account does not exist. ||---------||")
        else:
            print("\t\t\t||---------||  Loan Feature Off   ||---------||")


    def check_transaction_history(self, account_number):
        if account_number in self.users:
            print("\t\t\t||---------||  Transaction History: ||---------||")
            for transaction in self.users[account_number]['transactions']:
                print(transaction)
        else:
            print("\t\t\t||---------||    Account does not exist.     ||---------||")


class User:
    def __init__(self, bank, name, email, address, account_type):
        self.bank = bank
        self.account_number = bank.create_account(name, email, address, account_type)

    def user_deposit(self, amount):
        self.bank.deposit(self.account_number, amount)

    def user_withdraw(self, amount):
        self.bank.withdraw(self.account_number, amount)

    def user_check_balance(self):
        self.bank.check_balance(self.account_number)

    def user_check_transaction_history(self):
        self.bank.check_transaction_history(self.account_number)

    def user_take_loan(self, loan_amount):
        self.bank.take_loan(self.account_number, loan_amount)

    def user_transfer_money(self, to_account_number, amount):
        self.bank.transfer_money(self.account_number, to_account_number, amount)
        


class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, address, account_type):
        self.bank.create_account(name, email, address, account_type)

    def delete_account(self, account_number):
        self.bank.delete_account(account_number)

    def see_all_user_accounts(self):
        if self.bank.users:
            self.bank.show_all_accounts()
        else:
            print("\t\t\t||---------||  There are no user accounts. ||---------||")

    def check_total_balance(self):
        print(f"\t\t\t||---------|| Total Bank Balance: {self.bank.bank_balance}   ||---------||")
        
    def on_loan(self):
        if self.bank.loan_feature_enable:
            print("\t\t\t\t||---------||    Loan feature is already enabled. ||---------||")
        else:
            self.bank.loan_feature_enable = True
            print("\t\t\t\t||---------||    Loan feature has been enabled. ||---------||")

    def off_loan(self):
        if not self.bank.loan_feature_enable:
            print("\t\t\t||---------||  Loan feature is already disabled.    ||---------||")
        else:
            self.bank.loan_feature_enable = False
            print("\t\t\t||---------||  Loan feature has been disabled.    ||---------||")
        
    @property
    def total_loan(self):
        return self.bank.total_loan_amount


bank = Bank("AB Bank", 10000000000, 100000, 100, 100)

admin = Admin(bank)




def user_access():
    name = input("\tEnter Your Name: ")
    email = input("\tEnter Your Email: ")
    address = input("\tEnter Your Address: ")
    account_type = input("\tEnter Your Account Type: ")
    open_account = User(bank, name=name, email=email, address=address, account_type=account_type)
    
    task = True
    while task:
        
        print("\t\t1. Check Balance.")
        print("\t\t2. Deposit.")
        print("\t\t3. Withdraw.")
        print("\t\t4. Transfer money.")
        print("\t\t5. Check transaction History.")
        print("\t\t6. Take Loan.")
        print("\t\t7. Exit.")

        in_choice = input("\t\t\tEnter Your Option: ")
        if in_choice == '1':
            open_account.user_check_balance()
    

        elif in_choice == '2':
            amount = int(input("\n\t\t\tEnter Your Deposit Amount: "))
            open_account.user_deposit(amount)

        elif in_choice == '3':
            amount = int(input("\n\t\t\tEnter Your Withdraw Amount: "))
            open_account.user_withdraw(amount)

        elif in_choice == '4':
            account_number = int(input("\n\t\t\tEnter her/him account number for transfer money: "))
            amount = int(input("\n\t\t\tEnter Your amount for transfer money: "))
            open_account.user_transfer_money(account_number, amount)

        elif in_choice == '5':
            open_account.user_check_transaction_history()

        elif in_choice == '6':
            amount = int(input("\n\t\t\tEnter Your amount for take loan: "))
            open_account.user_take_loan(amount)
        elif in_choice == '7':
            task = False
            break
        else:
            print("Please Enter the correct Option!!")


def admin_access():
    task = True
    while task:
        print("\t1. See All User.")
        print("\t2. Check Total Balance in Bank.")
        print("\t3. On loan Feature.")
        print("\t4. Off loan feature.")
        print("\t5. Create Account.")
        print("\t6. Delete account.")
        print("\t7. To see how much money has been loaned.")
        print("\t8. Exit.")
        
        choice = input("\t\tEnter Your choice: ")
        
        if choice == '1':
            admin.see_all_user_accounts()
        
        elif choice == '2':
            admin.check_total_balance()
        
        elif choice == '3':
            admin.on_loan()
        
        elif choice == '4':
            admin.off_loan()
        
        elif choice == '5':
            name = input("\t\tEnter User Name: ")
            email = input("\t\tEnter User Email: ")
            address = input("\t\tEnter User Address: ")
            account_type = input("\t\tEnter User Account Type: ")
            
            admin.create_account(name=name, email=email, address=address, account_type=account_type)
        
        elif choice == '6':
            account_number = int(input("\t\tEnter account number for delete account: "))
            admin.delete_account(account_number)
        
        elif choice == '7':
            print(f"\n\t\tTotal Loan Amount: {admin.total_loan}")
        
        elif choice == '8':
            task = False
            break
        
        else:
            print("Please Enter the correct Option!!")


run = True
while run:
    print("\n\n**************WELCOME*************\n\n")
    print("1. User access")
    print("2. Admin access")
    print("3. Exit")
    
    option = input("Enter Your Option: ")
    
    if option == '1':
        user_access()
    
    elif option == '2':
        admin_access()
    
    elif option == '3':
        run = False
        break
    else:
        print("Please Enter the correct Option!!")