# JetbrainBankingDatabase
This is a simple banking system, which can create creditcard number (the number are 16 digits and are checked with Luhn-algorithm) and pin. The created info will be stored in a database and can be deleted if wanted.
Function of the system:
1) Create credit card and pin
2) Login into the created account
3) Different error such as wrong pin or wrong card number will be handle
4) Showing balance for choosed account
5) Adding balance into choosed account
6) Transfer money to another account within the database
.Here some situation will be handle. Such as enter a wrong transfering account, not enough fund, the cardnumber not mached with Luhn algorithm, 
8) Close the account (delete from database)
The programm will interact with database and have a user interface. The user interface will keep on running until the user want to stop the programm by entering '0'
