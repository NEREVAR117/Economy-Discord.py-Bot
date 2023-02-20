




# 9pm - Jackpot clears out

# 11:57 - Companies history
# 11:59 - Member history

# 12:01 - Education detagger
# 12:03 - Bank interest
# 12:05 - Stocks adjustment

# 4am - Lottery resets







# Updates the post in REMOVED FOR GITHUB's server to reflect the richest members once a minute
async def richest_post_updater(sqlite3, asyncio, client):
    db_conn = sqlite3.connect('economy_game.db')
    theCursor = db_conn.cursor()

    await asyncio.sleep(10)

    while True:

        list_of_members = db_conn.execute("SELECT * FROM Members")
        list_of_members = list_of_members.fetchall()

        # Sorts the list of members by highest to lowest money
        list_of_members = sorted(list_of_members, key=lambda x: x[3], reverse=True)

        # Prints to console, in order, the richest members
        top_members_post = '```The richest in the server: \n\n'
        for member in list_of_members:

            # Rounds to 2 decimal places (otherwise it will print something like 30.0911111111111)
            net_worth = "%.2f" % round(member[3], 2)
            money = "%.2f" % round(member[4], 2)
            bank = "%.2f" % round(member[5], 2)
            stock_value = "%.2f" % round(member[6], 2)

            top_members_post += member[1] + "'s net worth: " + net_worth + "$.  [Money: " + money + "$]  [Bank: " + bank + "$]  [Stocks: " + stock_value + "$]\n"

        top_members_post += '```'

        channel = client.get_channel(REMOVED FOR GITHUB)
        message_to_edit = await channel.fetch_message(REMOVED FOR GITHUB)

        await message_to_edit.edit(content=top_members_post)

        await asyncio.sleep(60)






# Updates the post in REMOVED FOR GITHUB's server to reflect general company and stock information once a minute
async def stocks_post_updater(sqlite3, asyncio, client):
    db_conn = sqlite3.connect('economy_game.db')
    theCursor = db_conn.cursor()

    await asyncio.sleep(10)

    while True:
        companies = db_conn.execute('SELECT * FROM Companies')
        companies = companies.fetchall()

        channel = client.get_channel(REMOVED FOR GITHUB)
        message_to_edit = await channel.fetch_message(REMOVED FOR GITHUB)

        await message_to_edit.edit(content='```   The current company stock information is:\n' +
            '[1]  BDSM Planet                  [Company Value: ' + str(companies[0][2]) + '$] [Available Stock: ' + str(companies[0][4]) + ' / ' + str(companies[0][3]) + '] [Stock Price: ' + str(companies[0][5]) + '$]\n' +
            '[2]  Christian Mingle             [Company Value: ' + str(companies[1][2]) + '$] [Available Stock: ' + str(companies[1][4]) + ' / ' + str(companies[1][3]) + '] [Stock Price: ' + str(companies[1][5]) + '$]\n' +
            '[3]  Hand-Drawn Frames Studios    [Company Value: ' + str(companies[2][2]) + '$] [Available Stock: ' + str(companies[2][4]) + ' / ' + str(companies[2][3]) + '] [Stock Price: ' + str(companies[2][5]) + '$]\n' +
            '[4]  Honnoji Academy              [Company Value: ' + str(companies[3][2]) + '$] [Available Stock: ' + str(companies[3][4]) + ' / ' + str(companies[3][3]) + '] [Stock Price: ' + str(companies[3][5]) + '$]\n' +
            '[5]  REMOVED FOR GITHUB Co.                     [Company Value: ' + str(companies[4][2]) + '$] [Available Stock: ' + str(companies[4][4]) + ' / ' + str(companies[4][3]) + '] [Stock Price: ' + str(companies[4][5]) + '$]\n\n' +

            '[6]  Ligma Beans                  [Company Value: ' + str(companies[5][2]) + '$] [Available Stock: ' + str(companies[5][4]) + ' / ' + str(companies[5][3]) + '] [Stock Price: ' + str(companies[5][5]) + '$]\n' +
            '[7]  Military Industrial Complex  [Company Value: ' + str(companies[6][2]) + '$] [Available Stock: ' + str(companies[6][4]) + ' / ' + str(companies[6][3]) + '] [Stock Price: ' + str(companies[6][5]) + '$]\n' +
            '[8]  National Propane Association [Company Value: ' + str(companies[7][2]) + '$] [Available Stock: ' + str(companies[7][4]) + ' / ' + str(companies[7][3]) + '] [Stock Price: ' + str(companies[7][5]) + '$]\n' +
            '[9]  Obama United                 [Company Value: ' + str(companies[8][2]) + '$] [Available Stock: ' + str(companies[8][4]) + ' / ' + str(companies[8][3]) + '] [Stock Price: ' + str(companies[8][5]) + '$]\n' +
            '[10] Sorcerers of the Toast       [Company Value: ' + str(companies[9][2]) + '$] [Available Stock: ' + str(companies[9][4]) + ' / ' + str(companies[9][3]) + '] [Stock Price: ' + str(companies[9][5]) + '$]```')





        await asyncio.sleep(60)














# Updates the net worth of users every minute, set off by 30 seconds, in the database 30 seconds into every minute
async def net_worth_database_updater(sqlite3, datetime, asyncio):

    db_conn = sqlite3.connect('economy_game.db')
    theCursor = db_conn.cursor()

    while True:
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%S")

        if current_time == '30':

            all_users = db_conn.execute("SELECT User_ID FROM Members")
            all_users = all_users.fetchall()

            # Updates the winner's and lottery ticker receivers' Net Worth
            for user in all_users:

                user_id = user[0]

                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(user_id))
                money = money.fetchone()

                bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(user_id))
                bank = bank.fetchone()

                stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(user_id))
                stock_value = stock_value.fetchone()

                net_worth = money[0] + bank[0] + stock_value[0]

                db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(user_id))
                db_conn.commit()

            print("Successfully updated all net worths at 30 seconds")




        await asyncio.sleep(1)


# net_worth_database_updater_task = asyncio.ensure_future(net_worth_database_updater())

# TURN THIS ON IF NET WORTHS AREN'T FULLY UPDATING WITH THINGS SOME TIMES





















# Jackpot function to pay out once a day the winner (if there is one) at 9pm
async def jackpot_payout(datetime, sqlite3, random, client, asyncio):

    # Time each day to trigger
    time_to_trigger = datetime.time(hour=21, minute=0)

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        if str(time_to_trigger) == current_time:
            # This may need to be moved in the outer scope??
            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            # Gets the sum of the total jackpot to pay it to the winner
            jackpot_payout = db_conn.execute("SELECT SUM(Jackpot_Amount) FROM Members")
            jackpot_payout = jackpot_payout.fetchone()
            jackpot_payout = jackpot_payout[0]

            # Checks if there's even a jackpot going
            if jackpot_payout == 0.0:
                print("No jackpot payout... skipping.")

            else:
                # Gets a list of people that were in the jackpot
                jackpot_winners = db_conn.execute("SELECT Username FROM Members WHERE Jackpot_Amount > 0.0")
                jackpot_winners = jackpot_winners.fetchall()
                print("Potential winners are:", jackpot_winners)
                jackpot_winner = random.choice(jackpot_winners)
                jackpot_winner = jackpot_winner[0]
                print("Winner is:", jackpot_winner)

                # Pays the winner the jackpot amount
                money = db_conn.execute('SELECT Money FROM Members WHERE Username = ?', (jackpot_winner,))
                money = money.fetchone()
                print(money)
                money = money[0] + jackpot_payout
                print(money)


                db_conn.execute("UPDATE Members SET Money = ? WHERE Username = ?", (money, jackpot_winner))
                db_conn.commit()

                print("derp")

                # Resets the Jackpot_Amount column to 0.0
                db_conn.execute("Update Members SET Jackpot_Amount = 0.0")
                db_conn.commit()

                # Posts to REMOVED FOR GITHUB's channel the payout, who won it, the amount, and lottery ticket payouts, etc.
                channel = client.get_channel(REMOVED FOR GITHUB)

                print("Successfully paid out the jackpot to " + jackpot_winner + " for amount of " + str(jackpot_payout) + "$.")


                # Checks if each user paid in at least 30$ to trigger people getting lottery winnings
                money_check = jackpot_payout / len(jackpot_winners)

                print("money check is", money_check)

                if money_check < 30.0 or len(jackpot_winners) == 1:
                    await channel.send(jackpot_winner + " won the jackpot! They received " + str(jackpot_payout) + "$.")


                else:
                    await channel.send(jackpot_winner + " won the jackpot! They received " + str(jackpot_payout) + "$. All participants were also rewarded with 1$ lottery tickets!")

                    # Lottery 10 average payout = 10.50$ (105%)
                    lottery_10_winnings = [*(11 * [0]), *(7 * [1]), *(14 * [2]), *(19 * [5]), *(26 * [10]), *(18 * [20]), *(4 * [50]), *(1 * [100])]

                    message_to_post = "The lottery winnings are: "

                    # Gets each participants lottery payout and also updates them in the database
                    for user in jackpot_winners:
                        user = user[0]

                        lottery_payout = random.choice(lottery_10_winnings)

                        print(user)

                        message_to_post += user + " won " + str(lottery_payout) + "$ | "

                        print("roll 1)")

                        money = db_conn.execute("SELECT Money FROM Members WHERE Username = ?", (user,))
                        money = money.fetchone()
                        money = money[0]

                        print("roll 1)")

                        money += lottery_payout

                        print(money)

                        db_conn.execute("UPDATE Members SET Money = ? WHERE Username = ?", (money, user))

                    print('test')

                    db_conn.commit()

                    # Appends end of the string to remove excess |
                    message_to_post = message_to_post[:-3]

                    await asyncio.sleep(3)

                    await channel.send(message_to_post)

                print("pre test thing")

                # Updates the winner's and lottery ticker receivers' Net Worth
                for user in jackpot_winners:

                    print("user is", user[0])

                    winner_id = db_conn.execute("SELECT User_ID FROM Members WHERE Username = ?", (user[0],))
                    winner_id = winner_id.fetchone()
                    winner_id = winner_id[0]

                    print("Winner ID is", winner_id)

                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(winner_id))
                    money = money.fetchone()

                    bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(winner_id))
                    bank = bank.fetchone()

                    stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(winner_id))
                    stock_value = stock_value.fetchone()

                    net_worth = money[0] + bank[0] + stock_value[0]

                    db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(winner_id))
                    db_conn.commit()

                print("Successfully did the payout (including updating net worth(s))")


        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)













# Once a week on Sunday at 11:30pm people with stocks are paid dividen payments of profit over the last week
async def stock_dividend_payout(datetime, sqlite3, client, asyncio):

    # Time each day to trigger (11:30pm)
    time_to_trigger = datetime.time(hour=23, minute=30)

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        # Triggers only on Sundays
        if str(time_to_trigger) == current_time and datetime.date.today().weekday() == 6:

            # This may need to be moved in the outer scope??
            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            stocks_data = db_conn.execute("SELECT * FROM Members")
            stocks_data = stocks_data.fetchall()

            # Cycles through each member's stock data
            for member_stocks in stocks_data:

                # Determines the value of the dividend payout
                weekly_dividend = member_stocks[6] * 0.025
                weekly_dividend = round(weekly_dividend, 2)

                # Only reports (DM's) to people, and updates their earnings, if they have stock at all
                if weekly_dividend != 0.0:
                    # Messages the user
                    user = client.get_user(member_stocks[0])
                    await user.send("Your weekly stock dividends payout is: " + str(weekly_dividend) + "$")

                    # Updates their net worth and money
                    db_conn.execute('UPDATE Members SET Bank = Bank + ? WHERE User_ID = ?', (weekly_dividend, member_stocks[0]))
                    db_conn.execute('UPDATE Members SET Net_Worth = Net_Worth + ? WHERE User_ID = ?', (weekly_dividend, member_stocks[0]))
                    db_conn.commit()


        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)











# Function to log company stocks once a day at 11:57pm
async def stocks_history_logging(datetime, sqlite3, time, asyncio):

    # Time each day to trigger (Shortly before midnight)
    time_to_trigger = datetime.time(hour=23, minute=57) # 11:57pm

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        # Only triggers if it's the relevant time
        if str(time_to_trigger) == current_time:

            # This may need to be moved in the outer scope??
            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            companies_database = db_conn.execute("SELECT * FROM Companies")
            companies_database = companies_database.fetchall()

            unix_time = time.time()

            # Pushes into the Stocks_History table the relevant information
            for inner_list in companies_database:

                db_conn.execute("INSERT INTO Companies_History (Company_Name, Total_Value, Max_Stocks, Available_Stocks, Stocks_Value, Market_Trend, Date, Time_Of) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (inner_list[0], inner_list[2], inner_list[3], inner_list[4], inner_list[5], inner_list[6], datetime.date.today(), unix_time))


            # Pushes Everyone's money record into the Members_History table
            all_value_sum = db_conn.execute("SELECT SUM(Total_Value) FROM Companies")
            all_value_sum = all_value_sum.fetchone()
            all_value_sum = all_value_sum[0]

            all_value_sum = "%.2f" % round(all_value_sum, 2)

            db_conn.execute("INSERT INTO Companies_History (Company_Name, Total_Value, Max_Stocks, Available_Stocks, Stocks_Value, Market_Trend, Date, Time_Of) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("All Market Value", all_value_sum, 0, 0, 0, 0, datetime.date.today(), unix_time))
            db_conn.commit()


        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)












# Function to log people's money once per day at 11:59pm
async def members_history_logging(datetime, sqlite3, time, asyncio):

    # Time each day to trigger (Shortly before midnight)
    time_to_trigger = datetime.time(hour=23, minute=59)

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        # Only triggers if it's the relevant time
        if str(time_to_trigger) == current_time:
            # This may need to be moved in the outer scope??
            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            members_database = db_conn.execute("SELECT * FROM Members")
            members_database = members_database.fetchall()

            unix_time = time.time()

            # Pushes into the Members_History Table the relevant information
            for inner_list in members_database:

                # These can't be re-assigned to themselves due to being tuples
                net_worth = "%.2f" % round(inner_list[3], 2)
                money = "%.2f" % round(inner_list[4], 2)
                bank = "%.2f" % round(inner_list[5], 2)
                stock_value = "%.2f" % round(inner_list[6], 2)

                db_conn.execute("INSERT INTO Members_History (User_ID, Username, Nickname, Net_Worth, Money, Bank, Stock_Value, Date, Time_Of) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (inner_list[0], inner_list[1], inner_list[2], net_worth, money, bank, stock_value, datetime.date.today(), unix_time))
                #db_conn.commit()

            # Commit it before retrieving data again just below
            db_conn.commit()

            # Pushes Everyone's Total Net Worth record into the Members_History Table
            net_worth_sum = db_conn.execute("SELECT SUM(Net_Worth) FROM Members")
            net_worth_sum = net_worth_sum.fetchone()
            net_worth_sum = net_worth_sum[0]

            net_worth_sum = "%.2f" % round(net_worth_sum, 2)

            print("Total net worth is:", net_worth_sum)

            db_conn.execute("INSERT INTO Members_History (User_ID, Username, Nickname, Net_Worth, Date, Time_Of) VALUES (?, ?, ?, ?, ?, ?)", (0, "Everyone", "Everyone", net_worth_sum, datetime.date.today(), unix_time))
            db_conn.commit()


        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)















# Removes the 'once a day' tag for people studying at AND company influence tag AND stock bought tags at 12:01am
async def education_detagger(datetime, sqlite3, asyncio):

    # Time each day to trigger (Shortly after midnight)
    time_to_trigger = datetime.time(hour=0, minute=1) # 12:01am

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        # Only triggers if it's the relevant time
        if str(time_to_trigger) == current_time:

            # This may need to be moved in the outer scope??
            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            member_table = db_conn.execute("SELECT * FROM Members")
            member_table = member_table.fetchall()

            for member_data in member_table:
                if '.day_wait' in member_data[10]:

                    replacement = member_data[10]
                    replacement = replacement.split('.')
                    replacement = replacement[0]

                    db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (replacement, member_data[0]))

            db_conn.commit()

            print("Triggered education daily detagger")

            # Resets the daily company influencer tag
            db_conn.execute("UPDATE Companies SET Daily_Influence = ?", ('None',))
            db_conn.commit()

            print("Successfully removed daily influence tag from Companies Table")

            # Resets the daily stocks bought tag
            db_conn.execute("UPDATE Members SET Stocks_Bought = ?", ('None',))
            db_conn.commit()

            print("Successfully removed stocks bought tag from Members Table")




        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)















# Money in the bank accrues some interest at 12:03am
async def bank_interest_accruer(datetime, sqlite3, asyncio):

    # Time each day to trigger (Shortly before midnight)
    time_to_trigger = datetime.time(hour=0, minute=3) # 12:03am

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        # Only triggers if it's the relevant time
        if str(time_to_trigger) == current_time:

            # This may need to be moved in the outer scope??
            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            members_table = db_conn.execute('SELECT * FROM Members')
            members_table = members_table.fetchall()

            # Loop to check and update all members' bank accounts
            for member_data in members_table:
                bank = member_data[5]

                # Logical flow deciding what to do with the money (depending on how much it is)
                if bank >= 1000 and bank < 10000:
                    print("Between 1,000 and 10,000")
                    bank = bank * 1.01

                elif bank >= 10000 and bank < 100000:
                    print("Between 10,000 and 100,000")
                    bank = bank * 1.02

                elif bank >= 100000 and bank < 1000000:
                    print("Between 100,000 and 1,000,000")
                    bank = bank * 1.03

                elif bank >= 1000000 and bank < 10000000:
                    print("Between 1,000,000 and 10,000,000")
                    bank = bank * 1.04

                elif bank >= 10000000 and bank < 100000000:
                    print("Between 10,000,000 and 100,000,000")
                    bank = bank * 1.05

                elif bank >= 100000000 and bank < 1000000000:
                    print("Between 100,000,000 and 1,000,000,000")
                    bank = bank * 1.06

                elif bank >= 1000000000 and bank < 10000000000:
                    print("Between 1,000,000,000 and 10,000,000,000")
                    bank = bank * 1.07

                elif bank >= 10000000000 and bank < 100000000000:
                    print("Between 10,000,000,000 and 100,000,000,000")
                    bank = bank * 1.08

                elif bank >= 100000000000 and bank < 1000000000000:
                    print("Between 100,000,000,000 and 1,000,000,000,000")
                    bank = bank * 1.09

                elif bank >= 1000000000000 and bank < 10000000000000:
                    print("More than 1,000,000,000,000!!!")
                    bank = bank * 1.10

                # Formats and updates the bank account
                bank = float("%.2f" % round(bank, 2))
                db_conn.execute("UPDATE Members SET Bank = ? WHERE User_ID = ?", (bank, member_data[0]))

                # We need to format and update the net worth too
                net_worth = member_data[4] + bank + member_data[6]
                net_worth = float("%.2f" % round(net_worth, 2))
                db_conn.execute("UPDATE Members SET Net_Worth=  ? WHERE User_ID = ?", (net_worth, member_data[0]))



            # After all the cycles of updating the bank, it now commits it
            db_conn.commit()



        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)














# Once a day the stock market is updated to reflect its trends and alter the company values at 12:05am
async def stock_market_updater(datetime, asyncio, sqlite3, random):

    # Time each day to trigger
    time_to_trigger = datetime.time(hour=0, minute=5) # 12:05am

    await asyncio.sleep(10)

    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        if str(time_to_trigger) == current_time:

            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            print("Successfully updating the stock market.")

            companies_list = db_conn.execute("SELECT * FROM Companies")
            companies_list = companies_list.fetchall()
            print(companies_list)

            for sub_company_list in companies_list:
                print(sub_company_list[6])

                print(sub_company_list[0])

                # Checks if the company's market trend is hitting a rest period before climbing or descending
                if sub_company_list[6] == 0:

                    print("Equals 0")

                    # 60% chance is stays on 0
                    keep_zero_factor = random.randint(1, 5)

                    if keep_zero_factor == 1 or keep_zero_factor == 2 or keep_zero_factor == 3:
                        print("Stayed on 0")
                        market_trend = 0

                    else:
                        market_trend = random.randint(-10, 10)

                    market_fluctuation = random.uniform(0.99, 1.01)

                # Checks if the company is still in a upward swing
                elif sub_company_list[6] > 0:

                    print("Greater than 0")

                    # Checks if the current value is double or more than the original value, and tries to slow it
                    if sub_company_list[2] > sub_company_list[1] * 2:
                        print("More than double original value, slowing upward swing...")
                        market_fluctuation = random.uniform(1.01, 1.06)

                    else:
                        market_fluctuation = random.uniform(1.01, 1.08)

                    market_trend = sub_company_list[6] - 1

                # Checks if the company is still in a downward swing
                elif sub_company_list[6] < 0:

                    print("Less than 0")

                    # Checks if the current value is half or less than the original value, and tries to slow it
                    if sub_company_list[2] < sub_company_list[1] / 2:

                        print("Less than half original value, slowing downward swing...")
                        market_fluctuation = random.uniform(0.94, 0.99)

                    else:
                        market_fluctuation = random.uniform(0.92, 0.99)

                    market_trend = sub_company_list[6] + 1

                print("DB execution")
                db_conn.execute("UPDATE Companies SET Market_Trend = ? WHERE Company_Name = ?", (market_trend, sub_company_list[0]))


                total_value = round(sub_company_list[2] * market_fluctuation)
                #total_value = sub_company_list[2]
                print("total value is", total_value)

                db_conn.execute("UPDATE Companies SET Total_Value = ? WHERE Company_Name = ?", (total_value, sub_company_list[0]))

                stock_value = round(total_value / sub_company_list[3], 2)
                print("stock value is", stock_value)

                db_conn.execute("UPDATE Companies SET Stock_Value = ? WHERE Company_Name = ?", (stock_value, sub_company_list[0]))

            db_conn.commit()



            # Updates all users' Stock Value and Net Worth

            # Gets all members data and cycles through it
            members_data = db_conn.execute("SELECT * FROM Members")
            members_data = members_data.fetchall()

            for member in members_data:
                # Fetches the member's total owned stock count and their total worth
                stock_count = db_conn.execute("SELECT * FROM Stocks WHERE User_ID = " + str(member[0]))
                stock_count = stock_count.fetchone()

                # Removes the first 3 elements of the generated list
                stock_count = stock_count[3:]

                # Gets all the stock data from the Companies table
                companies = db_conn.execute('SELECT * FROM Companies')
                companies = companies.fetchall()

                # Loops through the list of companies/stock and adds them together as it goes
                total_stock_value = 0
                loop_count = 0

                for x in stock_count:
                    total_stock_value += stock_count[loop_count] * companies[loop_count][5]

                    loop_count += 1

                db_conn.execute("UPDATE Members SET Stock_Value = " + str(round(total_stock_value, 2)) + " WHERE User_ID = " + str(member[0]))
                db_conn.commit()

                # Gets and then updates the user's Net Worth
                net_worth = member[4] + member[5] + member[6]

                db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(member[0]))
                db_conn.commit()





        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)



















# Have a random event happen to a member, sometimes, twice a day at 8am and 8pm
async def random_member_event(datetime, sqlite3, random, client, asyncio):
    # Time each day to trigger
    time_to_trigger = datetime.time(hour=8, minute=0) # 8am
    time_to_trigger_2 = datetime.time(hour=20, minute=0) # 8pm


    # Loops once a second to check the time
    while True:

        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%H:%M:%S")

        if str(time_to_trigger) == current_time or str(time_to_trigger_2) == current_time:
        # If current_time == current_time:

            db_conn = sqlite3.connect('economy_game.db')
            theCursor = db_conn.cursor()

            # Gets all members data and cycles through it
            members_data = db_conn.execute("SELECT * FROM Members")
            members_data = members_data.fetchall()

            chosen_member_data = random.choice(members_data)

            print(chosen_member_data)

            channel = client.get_channel(REMOVED FOR GITHUB)

            # 12.5% of an event happening twice per day (so 25% total of it happening at least once a day)
            event_chance = random.randint(1, 8)

            print("Event chance", event_chance)

            if event_chance == 1:

                # Decides what event happens
                event_type = random.randint(1, 4)

                print("Event type", event_type)

                # User finds some money on the ground
                if event_type == 1:

                    dollars_to_be_found = [1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 10, 10, 10, 10, 20, 20, 20, 50, 50, 100]
                    dollars_found = random.choice(dollars_to_be_found)

                    money = chosen_member_data[4] + dollars_found

                    db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, chosen_member_data[0]))
                    db_conn.commit()

                    await channel.send(chosen_member_data[1] + " found " + str(dollars_found) + "$ on the ground.")

                # User loses some money
                if event_type == 2:

                    dollars_to_be_lost = [1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 20, 20, 20, 20, 50, 50, 100] # Losing 50$ or 100$ is slightly less likely than finding them
                    dollars_lost = random.choice(dollars_to_be_lost)

                    # Checks if the user even has this much money on them
                    if chosen_member_data[4] == 0:
                        print("User had no money on them to lose.")
                        money = chosen_member_data[4]

                    elif chosen_member_data[4] < dollars_lost:
                        print("User lost all their money on them.")

                        dollars_lost = chosen_member_data[4]

                        money = 0

                        await channel.send("When trying to get some taco bell, " + chosen_member_data[1] + " seems to have misplaced their wallet. They lost " + str(dollars_lost) + "$")

                    else:
                        print("User lost some money")

                        money = chosen_member_data[4] - dollars_lost
                        money = float("%.2f" % round(money, 2))

                        await channel.send("When opening their wallet, " + chosen_member_data[1] + " notices some money of theirs is missing. They appear to have lost " + str(dollars_lost) + "$")


                    db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, chosen_member_data[0]))
                    db_conn.commit()


                # Small bank error in the user's favor if they have over 50$ in the bank
                if event_type == 3:

                    # Checks if they have at least 50$ in the bank (only people with 50$ in the bank should get this benefit)
                    tax_return = random.randint(20, 80)

                    if chosen_member_data[5] >= 50:
                        print("User had 50$ or more to get bank error in their favor")
                        bank = chosen_member_data[5] + tax_return
                        print(bank)

                        await channel.send(chosen_member_data[1] + " receives a letter showing their bank has made an error in their favor. " + str(tax_return) + "$ has been deposited into their bank account.")

                        db_conn.execute("UPDATE Members SET Bank = ? WHERE Username = ?", (bank, chosen_member_data[0]))
                        db_conn.commit()

                    else:
                        print("User did not have enough money in bank account to get bank error in their favor")



                # Player is being robbed
                if event_type == 4:

                    member_inventory = db_conn.execute("SELECT * FROM Inventory WHERE User_ID = ?", (chosen_member_data[0],))
                    member_inventory = member_inventory.fetchone()

                    print(member_inventory)

                    # The chance, as a percentage, of the player being successfully robbed
                    rob_chance = 70

                    print(member_inventory[3])

                    if member_inventory[3] == 'Owned': # Checks for a Kirby
                        print("They have a kirby")
                        rob_chance -= 5

                    if member_inventory[5] == 'Owned': # Checks for a gun
                        rob_chance -= 30

                    if member_inventory[6] == 'Owned': # Checks for a suit
                        rob_chance += 5

                    if member_inventory[7] == 'Owned': # Checks for a car
                        rob_chance -= -20

                    print("The chance of being robbed is: " + str(rob_chance) + "%")

                    robbing = random.randint(1, 100)

                    print("Rob value is:", robbing)

                    # User has no money to be stolen
                    if chosen_member_data[4] == 0:
                        print("User had no money")
                        await channel.send(f"When out and about, a hooded figure approached {chosen_member_data[1]}, but they had no money on them to be stolen.")


                    # User gets robbed
                    if robbing <= rob_chance:
                        print("User is being robbed")

                        money = chosen_member_data[4]

                        print("Money is", money)

                        money_stolen_percentage = random.uniform(0.1, 0.7) # 10% to 70%

                        money_stolen = money * money_stolen_percentage

                        # Triggers so not -too much- money is ever stolen at once
                        if money_stolen > 500:
                            money_stolen = 500

                            money_stolen_percentage = random.uniform(0.9, 0.97)  # 90% to 97%

                            money_stolen = money_stolen * money_stolen_percentage


                        print("Money stolen is", money_stolen)

                        money -= money_stolen

                        money = float("%.2f" % round(money, 2))

                        print("Money is now", money)

                        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, chosen_member_data[0]))
                        db_conn.commit()

                        money_stolen = float("%.2f" % round(money_stolen, 2))

                        await channel.send(f"When out and about, a hooded figure approached {chosen_member_data[1]} and managed to steal {money_stolen} from them.")

                    # User is almost robbed but gets away
                    if robbing > rob_chance:
                        print("User was almost robbed by got away")
                        await channel.send(f"When out and about, a hooded figure approached {chosen_member_data[1]}, but they managed to scare off the thief or drive away.")



                # Updates the user's Net Worth
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(chosen_member_data[0]))
                money = money.fetchone()

                bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(chosen_member_data[0]))
                bank = bank.fetchone()

                stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(chosen_member_data[0]))
                stock_value = stock_value.fetchone()

                net_worth = money[0] + bank[0] + stock_value[0]

                db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(chosen_member_data[0]))
                db_conn.commit()






        # Keeps the loop from running too frequently to save on CPU cycles
        await asyncio.sleep(1)