import random

class Account:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.account_id = self.generate_account_id()
        self.balance = initial_balance
        self.transaction_history = []
        self.payees = set()
        self.log_transaction(f"Account created with balance ${self.balance}")

    def generate_account_id(self):
        return str(random.randint(10000000, 99999999))

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Amount must be positive.")
            return
        self.balance += amount
        self.log_transaction(f"Deposited ${amount}")
        print(f"✅ Deposited ${amount}. Current Balance: ${self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Amount must be positive.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        self.log_transaction(f"Withdrew ${amount}")
        print(f"✅ Withdrew ${amount}. Current Balance: ${self.balance}")

    def add_payee(self, payee_id):
        if payee_id == self.account_id:
            print("❌ Cannot add yourself as payee.")
        elif payee_id in self.payees:
            print("❌ Payee already added.")
        else:
            self.payees.add(payee_id)
            self.log_transaction(f"Payee added: {payee_id}")
            print("✅ Payee added successfully.")

    def transfer(self, amount, recipient):
        if recipient.account_id not in self.payees:
            print("❌ Payee not in your list.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        recipient.balance += amount
        self.log_transaction(f"Transferred ${amount} to {recipient.account_id}")
        recipient.log_transaction(f"Received ${amount} from {self.account_id}")
        print(f"✅ Transferred ${amount} to {recipient.name} (ID: {recipient.account_id})")

    def view_transaction_history(self):
        print(f"\n📒 Transaction History for {self.name} (ID: {self.account_id})")
        for entry in self.transaction_history:
            print(" -", entry)
        if not self.transaction_history:
            print(" - No transactions yet.")

    def view_details(self):
        print(f"\n👤 Account Holder: {self.name}")
        print(f"🆔 Account ID: {self.account_id}")
        print(f"💰 Balance: ${self.balance}")
        print(f"📇 Payees: {', '.join(self.payees) if self.payees else 'None'}")

    def log_transaction(self, description):
        self.transaction_history.append(description)

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter Account Holder Name: ")
        try:
            balance = float(input("Enter Initial Balance (or press Enter for $0): ") or 0)
        except ValueError:
            print("Invalid amount. Defaulting to $0.")
            balance = 0
        account = Account(name, balance)
        self.accounts[account.account_id] = account
        print(f"\n🎉 Account Created Successfully! Account ID: {account.account_id}")

    def find_account(self, acc_id):
        return self.accounts.get(acc_id)

    def menu(self):
        while True:
            print("\n==== Virtual Banking Menu ====")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Add Payee")
            print("5. Transfer Money")
            print("6. View Account Details")
            print("7. View Transaction History")
            print("8. Exit")

            choice = input("Select an option (1-8): ")

            if choice == '1':
                self.create_account()

            elif choice in ['2', '3', '4', '5', '6', '7']:
                acc_id = input("Enter Your Account ID: ")
                account = self.find_account(acc_id)
                if not account:
                    print("❌ Account not found.")
                    continue

                if choice == '2':
                    amount = float(input("Enter deposit amount: "))
                    account.deposit(amount)

                elif choice == '3':
                    amount = float(input("Enter withdrawal amount: "))
                    account.withdraw(amount)

                elif choice == '4':
                    payee_id = input("Enter Payee Account ID to add: ")
                    if payee_id in self.accounts:
                        account.add_payee(payee_id)
                    else:
                        print("❌ Payee account does not exist.")

                elif choice == '5':
                    payee_id = input("Enter Payee Account ID: ")
                    recipient = self.find_account(payee_id)
                    if not recipient:
                        print("❌ Payee account not found.")
                        continue
                    amount = float(input("Enter amount to transfer: "))
                    account.transfer(amount, recipient)

                elif choice == '6':
                    account.view_details()

                elif choice == '7':
                    account.view_transaction_history()

            elif choice == '8':
                print("👋 Thank you for using Virtual Banking. Goodbye!")
                break
            else:
                print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    bank = BankSystem()
    bank.menu()
