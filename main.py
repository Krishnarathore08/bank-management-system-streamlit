"""
1. Create class Bank
2. CRUD Operation
Create -> Creating User Details
Read -> Reading User Details
Update -> Updating User Details
Delete -> Deleting User Details
"""


from pathlib import Path
import json
import random
import string

class Bank:
    database = "data.json"
    data = [] #YE data json me save hoga

    try:
        if Path(database).exists():
            print("File Exits..")
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("No such file exists...")
    except Exception as err:
        print("Error Occured")

    @classmethod
    def update(cls):
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod 
    def generateAcc():
        digits = random.choices(string.digits, k=4)
        alpha = random.choices(string.ascii_letters, k=4)
        id = digits + alpha
        random.shuffle(id)
        return "".join(id)

    #Create User
    def CreateAccount(self):
        info = {
            'name' : input("Enter your name : "),
            'age' : int(input("Enter your age : ")),
            'phoneNumber' : int(input("Enter your Number : ")),
            'email' : input("Enter your Email : "),
            'pin' : int(input("Enter your Pin : ")),
            'accountNumber' : Bank.generateAcc(),
            'balance' : 0
        }
        if info['age'] > 18 and len(str(info['pin'])) == 4 and len(str(info['phoneNumber'])) == 10:    
            Bank.data.append(info)
            Bank.update()
            print('Data added in List')
        else:
            print("Credintials are not Valid!")
            print(Bank.data)

    def depositMoney(self):
        accountno = input("Enter your account no. : ")
        pin = int(input("Enter your 4 digit pin : "))

        user_data = [i for i in Bank.data if i['accountNumber'] == accountno and i['pin'] == pin]
        if user_data == False:
            print("User not Found")
        else:
            amount = int(input("Enter amount : "))
            if amount <= 0:
                print("Invalid Amount")
            elif amount > 10000:
                print("Invalid Amount!!")
            else:
                user_data[0]['balance'] += amount
                print("Amount Credited...")
                Bank.update()

    def withdrawMoney(self):
        accountno = input("Enter your account no. : ")
        pin = int(input("Enter your 4 digit pin : "))

        user_data = [i for i in Bank.data if i['accountNumber'] == accountno and i['pin'] == pin]
        if user_data == False:
            print("User not Found")
        else:
            amount = int(input("Enter amount : "))
            if amount <= 0:
                print("Invalid Amount")
            elif amount > 10000:
                print("Greater than 10000")
            else:
                if user_data[0]['balance'] < amount:
                    print("Insufficient Funds...")
                else:
                    user_data[0]['balance'] -= amount
                    Bank.update()
                    print("Amount Debited...")

    def details(self):
        accountno = input("Enter your account no. : ")
        pin = int(input("Enter your 4 digit pin : "))

        user_data = [i for i in Bank.data if i['accountNumber'] == accountno and i['pin'] == pin]
        if user_data == False:
            print("User not Found")
        else:
            for i in user_data[0]:
                print(i, user_data[0][i])

    def deleteAccount(self):
        accountno = input("Enter your account no. : ")
        pin = int(input("Enter your 4 digit pin : "))

        user_data = [i for i in Bank.data if i['accountNumber'] == accountno and i['pin'] == pin]
        if user_data == False:
            print("User not Found")
        else:
            print("Are you sure you want to delete your acccount? (Yes/No) : ")
            choice = input()

            if choice == 'Yes':
                ind = Bank.data.index(user_data[0])
                Bank.data.pop(ind)
                Bank.update()
                print("Account delete successfully")
            else:
                print("Operation Terminated")

    def updateDetalis(self):
        accountno = input("Enter your account no. : ")
        pin = int(input("Enter your 4 digit pin : "))

        user_data = [i for i in Bank.data if i['accountNumber'] == accountno and i['pin'] == pin]
        if user_data == False:
            print("User not Found")
        else:
            print("Aap Account No. aur Balance Update/Change nahi kar sakte ho")

            print("Enter your details to update or just press enter to skip them")

            new_data = {
                'name' : input("Enter your name : "),
                'phoneNumber' : input("Enter your Number : "),
                'email' : input("Enter your Email : "),
                'pin' : input("Enter your Pin : "),
            }

            if new_data['name'] == "":
                new_data['name'] = user_data[0]['name']

            if new_data['phoneNumber'] == "":
                new_data['phoneNumber'] = user_data[0]['phoneNumber']
            else:
                new_data['phoneNumber'] = int(new_data['phoneNumber'])

            if new_data['email'] == "":
                new_data['email'] = user_data[0]['email']

            if new_data['pin'] == "":
                new_data['pin'] = user_data[0]['pin']
            else:
                new_data['pin'] = int(new_data['pin'])

            new_data['accountNumber'] = user_data[0]['accountNumber']
            new_data['balance'] = user_data[0]['balance']

            user_data[0].update(new_data)
            Bank.update()
            

obj = Bank()
print("Press 1 for Creating Account")
print("Press 2 for Depositing Money")
print("Press 3 for Withdrawing Money")
print("Press 4 for Account Details")
print("Press 5 for Updating Account Details")
print("Press 6 for Deleting Account")

choice = int(input("Enter your Choice : "))

if choice == 1:
    obj.CreateAccount()

elif choice == 2:
    obj.depositMoney()

elif choice == 3:
    obj.withdrawMoney()

elif choice == 4:
    obj.details()

elif choice == 5:
    obj.updateDetalis()

elif choice == 6:
    obj.deleteAccount()
