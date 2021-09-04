import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id INT,
                number TEXT,
                pin TEXT,
                balance INT DEFAULT 0);""")
storage_info = []
count = 0
balance = 0

class CardNumber:
    def __init__(self, banknum):
        self.banknum = banknum

    def cardnumber_generator(self): #15 Digits without lastnumber
        list_customerid = []
        for i in range(9):  # Create customerID
            list_customerid.append(str(random.randrange(10)))
        customerid = ''.join(list_customerid)
        card_number = self.banknum + customerid
        return card_number

    def pinnumber_generator(self): #Pin generator
        list_pin = []
        for i in range(4):
            list_pin.append(str(random.randrange(10)))
        pinnum = ''.join(list_pin)
        return pinnum

    def Luhn_algo_checksum(self): #return the 16 Digit card after checked with Luhn algo
        list_int = []
        digit_15 = self.cardnumber_generator()
        for num in digit_15:
            list_int.append(int(num))
        for i in range(0, len(list_int), 2):
            list_int[i] = list_int[i] * 2
        for i in range(len(list_int)):
            if list_int[i] > 9:
                list_int[i] = list_int[i] - 9
        check_sum = (10 - (sum(list_int) % 10))
        if check_sum == 10:
            return digit_15 + '0'
        return digit_15 + str(check_sum)

class ActionWithAccount:
    def __init__(self):
        pass
    def balance_showing(self):
        cur.execute('SELECT balance FROM card WHERE number = (?) and pin = (?);',(card_input, pin_input))
        balance = cur.fetchone()
        return print('Balance:', balance[0])
    def add_income(self):
        print('Enter income:')
        income = int(input())
        cur.execute("""UPDATE card
                        SET balance = balance + (?)
                        WHERE number = (?) AND pin = (?);""", (income, card_input, pin_input))
        conn.commit()
        return print('Income was added!')

    def do_transfer(self):
        print('Transfer\nEnter card number:')
        card_input_transfer = input()
        tuple_cardnum = []
        cur.execute('SELECT number FROM card;')
        for num in cur.fetchall():
            tuple_cardnum.append(num[0])
        if self.Luhn_algo_checker(card_input_transfer) == False:
            print('Probably you made a mistake in the card number. Please try again!')
        elif card_input_transfer == card_input:
            print("You can't transfer money to the same account!")
        elif card_input_transfer not in tuple_cardnum:
            print('Such a card does not exist.')
        else:
            print('Enter how much money you want to transfer:')
            money_transfer = int(input())
            cur.execute('SELECT balance FROM card WHERE number = (?) AND pin =(?)',(card_input, pin_input))
            balance_now = cur.fetchone()[0]
            if money_transfer > int(balance_now):
                print('Not enough money!')
            else:
                print('Success!')
                cur.execute("""UPDATE card
                                SET balance = balance - (?)
                                WHERE number = (?) AND pin = (?);""", (money_transfer, card_input, pin_input))
                cur.execute("""UPDATE card
                                SET balance = balance + (?)
                                WHERE number = (?);""", (money_transfer, card_input_transfer))
                conn.commit()
    def Luhn_algo_checker(self,card_num):
        list_int = []
        for i in range(len(card_num)-1):
                list_int.append(int(card_num[i]))
        for i in range(0, len(list_int), 2):
            list_int[i] = list_int[i] * 2
        for i in range(len(list_int)):
            if list_int[i] > 9:
                list_int[i] = list_int[i] - 9
        if (sum(list_int) + int(card_num[-1])) % 10 == 0:
            return True
        else:
            return False
    def close_account(self):
        cur.execute('DELETE FROM card WHERE number = (?);', (card_input,))
        print('The account has been closed!')
        conn.commit()
    def log_out(self):
        pass


while True:
    print('1. Create an account\n2. Log into account\n0. Exit') #User interface
    choice = int(input())

    if choice == 1:
        account_creating = CardNumber('400000') #Object creating with Bank number 400000
        storage_info.append([account_creating.Luhn_algo_checksum(), #Saving Cardnumber and PIN
                             account_creating.pinnumber_generator()])

        cur.execute("""INSERT INTO card (id, number, pin)
                       VALUES (?, ?, ?);""", (count, storage_info[count][0], storage_info[count][1])) # Insert information into table card in Database
        conn.commit()

        print('Your card has been created\nYour card number:')
        print(storage_info[count][0])
        print('Your card PIN:')
        print(storage_info[count][1])
        count += 1

    elif choice == 2:
        card_input = input('Enter your card number:')
        pin_input = input('Enter your PIN:')
        if (card_input, pin_input) in cur.execute('SELECT number, pin FROM card;'):
            print('You have successfully logged in!')
            while True:
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                choice_2 = int(input())
                if choice_2 == 1:
                    balance = ActionWithAccount()
                    balance.balance_showing()
                elif choice_2 == 2:
                    action = ActionWithAccount()
                    action.add_income()
                elif choice_2 == 3:
                    transfer = ActionWithAccount()
                    transfer.do_transfer()
                elif choice_2 == 4:
                    close = ActionWithAccount()
                    close.close_account()
                    break
                elif choice_2 == 0:
                    print('Bye!')
                    exit()
        else:
            print('Wrong card number or PIN!')
            continue
    elif choice == 0:
        conn.close()
        break
