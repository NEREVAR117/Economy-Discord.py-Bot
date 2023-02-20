


async def BankPrompt(message):
    await message.channel.send("""Bank commands are the following:
    ```    -bank info          (display your bank account information and the types of bank accounts)
        -bank deposit X     (puts X dollars from your person into your bank account)
        -bank withdraw X    (removes X dollars from your account and puts onto your person)

        (-deposit X and -withdraw X also work, as well as replacing X with max or all to move all the money at once)```""")







async def Bank(message, db_conn):
    split_message = message.content.split()

    if split_message[1] == "info":
        await message.channel.send("""Placing your money into the bank has two key benefits. 1) Protecting your money from theft. 2) Accruing interest.
    Accounts that earn interest begin at 1,000 dollars. The interest rate increases with each new bracket of investment.
    1,000 = 1%
    10,000 = 2%
    100,000 = 3%
    etc...""")

    # Changes where in the user's split message to grab the money information
    if split_message[0] == "-deposit" or split_message[0] == "-withdraw":
        message_placement = 1

    else:
        message_placement = 2

    # If the user is trying to put money into their bank
    if split_message[0] == "-deposit" or split_message[1] == "deposit":
        money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
        money = money.fetchone()
        money = float(money[0])

        bank_account = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(message.author.id))
        bank_account = bank_account.fetchone()
        bank_account = float(bank_account[0])

        # To prevent an error we first check if they're using numbers or characters as the deposit amount
        if split_message[message_placement] == 'all' or split_message[message_placement] == 'max':

            # Posts before money is assigned to 0
            await message.channel.send("You successfully deposited " + str(round(money, 2)) + "$ into your account.")

            bank_account += money
            money = 0

        else:
            # Checks if they even have that much money
            if money < float(split_message[message_placement]):
                await message.channel.send("You don't have that much money on hand. What's up?")

            else:
                bank_account += float(split_message[message_placement])
                money -= float(split_message[message_placement])

                await message.channel.send("You successfully deposited " + split_message[message_placement] + "$ into your account.")

        # Rounds the bank account and money
        bank_account = round(bank_account, 2)
        money = round(money, 2)

        db_conn.execute("UPDATE Members SET Bank = ? WHERE User_ID = ?", (bank_account, message.author.id))
        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

        db_conn.commit()

    # If the user is trying to take money from their bank
    if split_message[0] == "-withdraw" or split_message[1] == "withdraw":
        money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
        money = money.fetchone()
        money = float(money[0])

        bank_account = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(message.author.id))
        bank_account = bank_account.fetchone()
        bank_account = float(bank_account[0])

        # To prevent an error we first check if they're using numbers or characters as the deposit amount
        if split_message[message_placement] == 'all' or split_message[message_placement] == 'max':

            # Posts before bank_account is assigned to 0
            await message.channel.send("You successfully withdrew " + str(bank_account) + "$ from your account.")

            money += bank_account
            bank_account = 0


        else:
            # Checks if their bank account even has that much money
            if bank_account < float(split_message[message_placement]):
                await message.channel.send("Your bank account doesn't have that much money. Are you trying to rob us?")

            else:
                bank_account -= float(split_message[message_placement])
                money += float(split_message[message_placement])

                await message.channel.send("You successfully withdrew " + split_message[message_placement] + "$ from your account.")

        # Rounds the bank account and money
        bank_account = round(bank_account, 2)
        money = round(money, 2)

        db_conn.execute("UPDATE Members SET Bank = ? WHERE User_ID = ?", (bank_account, message.author.id))
        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

        db_conn.commit()