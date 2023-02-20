


async def StocksPrompt(message):
    await message.channel.send('''```   The available stock commands are:
    -stocks list (this shows the list of companies and their number IDs
    -stocks buy  (company number) (stock count)
    -stocks sell (company number) (stock count)```''')






async def Stocks(message, db_conn, users_buying_stock, client, asyncio, random):
    split_message = message.content.split()

    if split_message[1] == 'help':
        await message.channel.send('''```   The available stock commands are:
                -stocks list (this shows the list of companies and their number IDs
                -stocks buy  (company number) (stock count)
                -stocks sell (company number) (stock count)```''')

    if split_message[1] == 'list':
        companies = db_conn.execute('SELECT * FROM Companies')
        companies = companies.fetchall()

        await message.channel.send('```   The companies you can invest in are:\n' +
                                   '[1]  BDSM Planet                  [Company Value: ' + str(companies[0][2]) + '$] [Available Stock: ' + str(
            companies[0][4]) + ' / ' + str(companies[0][3]) + '] [Stock Price: ' + str(companies[0][5]) + '$]\n' +
                                   '[2]  Christian Mingle             [Company Value: ' + str(companies[1][2]) + '$] [Available Stock: ' + str(
            companies[1][4]) + ' / ' + str(companies[1][3]) + '] [Stock Price: ' + str(companies[1][5]) + '$]\n' +
                                   '[3]  Hand-Drawn Frames Studios    [Company Value: ' + str(companies[2][2]) + '$] [Available Stock: ' + str(
            companies[2][4]) + ' / ' + str(companies[2][3]) + '] [Stock Price: ' + str(companies[2][5]) + '$]\n' +
                                   '[4]  Honnoji Academy              [Company Value: ' + str(companies[3][2]) + '$] [Available Stock: ' + str(
            companies[3][4]) + ' / ' + str(companies[3][3]) + '] [Stock Price: ' + str(companies[3][5]) + '$]\n' +
                                   '[5]  REMOVED FOR GITHUB Co.                     [Company Value: ' + str(companies[4][2]) + '$] [Available Stock: ' + str(
            companies[4][4]) + ' / ' + str(companies[4][3]) + '] [Stock Price: ' + str(companies[4][5]) + '$]\n\n' +

                                   '[6]  Ligma Beans                  [Company Value: ' + str(companies[5][2]) + '$] [Available Stock: ' + str(
            companies[5][4]) + ' / ' + str(companies[5][3]) + '] [Stock Price: ' + str(companies[5][5]) + '$]\n' +
                                   '[7]  Military Industrial Complex  [Company Value: ' + str(companies[6][2]) + '$] [Available Stock: ' + str(
            companies[6][4]) + ' / ' + str(companies[6][3]) + '] [Stock Price: ' + str(companies[6][5]) + '$]\n' +
                                   '[8]  National Propane Association [Company Value: ' + str(companies[7][2]) + '$] [Available Stock: ' + str(
            companies[7][4]) + ' / ' + str(companies[7][3]) + '] [Stock Price: ' + str(companies[7][5]) + '$]\n' +
                                   '[9]  Obama United                 [Company Value: ' + str(companies[8][2]) + '$] [Available Stock: ' + str(
            companies[8][4]) + ' / ' + str(companies[8][3]) + '] [Stock Price: ' + str(companies[8][5]) + '$]\n' +
                                   '[10] Sorcerers of the Toast       [Company Value: ' + str(companies[9][2]) + '$] [Available Stock: ' + str(
            companies[9][4]) + ' / ' + str(companies[9][3]) + '] [Stock Price: ' + str(companies[9][5]) + '$]\n\n' +

                                   '   Type   -stocks buy (company number ID here) (amount of stocks to buy here) to purchase your stocks. There is a 5% tax!```')

    # Old dictionary using brackets

    ###stock_companies = {'[1]': 'BDSM Planet', '[2]': 'Christian Mingle', '[3]': 'Hand-Drawn Frames Studios',
    ###                   '[4]': 'Honnoji Academy', '[5]': 'REMOVED FOR GITHUB Co.', '[6]': 'Ligma Beans',
    ###                   '[7]': 'Military Industrial Complex', '[8]': 'National Propane Association',
    ###                   '[9]': 'Obama United', '[10]': 'Sorcerers of the Toast'}

    stock_companies = {'1': 'BDSM Planet', '2': 'Christian Mingle', '3': 'Hand-Drawn Frames Studios',
                       '4': 'Honnoji Academy', '5': 'REMOVED FOR GITHUB Co.', '6': 'Ligma Beans',
                       '7': 'Military Industrial Complex', '8': 'National Propane Association',
                       '9': 'Obama United', '10': 'Sorcerers of the Toast'}

    # Triggers if the user is trying to buy stock
    if split_message[1] == 'buy':

        # Checks if the person is already trying to buy/sell stocks to prevent stock spam
        if message.author.id in users_buying_stock:
            await message.channel.send("You're already in the process of buying/selling stocks. Finish that first.")

        else:
            # Checks if the user is trying to buy less than 1 stock
            if int(split_message[3]) < 1:
                await message.channel.send("You need to buy at least 1 stock, bro.")

            else:

                # First checks if the user even has enough money
                company_name = stock_companies[split_message[2]]

                # Gets the current stock value
                stock_value = db_conn.execute('SELECT Stock_Value FROM Companies WHERE Company_Name = ?', (company_name,))
                stock_value = stock_value.fetchone()
                stock_value = float(stock_value[0])

                # Gets the user's available money
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                money = money.fetchone()
                money = float(money[0])

                # Multiplies the purchase cost by 1.05 to add the 5% tax. May need to be moved deeper into the logic?
                if money < (stock_value * int(split_message[3]) * 1.05):
                    await message.channel.send("Yeah, no. You don't have that kind of money.")

                else:
                    # Checks if there's even that much stock available
                    available_stock = db_conn.execute('SELECT Available_Stocks FROM Companies WHERE Company_Name = ?', (company_name,))
                    available_stock = available_stock.fetchone()
                    available_stock = float(available_stock[0])

                    if available_stock < int(split_message[3]):
                        await message.channel.send("You're trying to buy more stock than what's available.")

                    else:
                        # Once all above checks have been met, we place the user into the buying_Stocks list
                        users_buying_stock.append(message.author.id)

                        user_payment_amount = stock_value * int(split_message[3])
                        tax_amount = round(user_payment_amount * 0.05, 2)
                        total_amount_due = round(user_payment_amount + tax_amount, 2)

                        # Prompts the user for how much they'll be spending, and asks for them to confirm
                        bot_message = await message.channel.send(
                            "You're attempting to buy " + split_message[3] + " stock(s) from the company " + stock_companies[
                                split_message[2]] + ". " +
                            "Each stock has a value of " + str(stock_value) + "$, totalling your request stock value out to " + str(
                                round(user_payment_amount, 2)) + "$ with a 5% tax (" + str(tax_amount) + "$), equaling a total of " + str(
                                total_amount_due) + "$ due for purchase." +
                            "\nPlease type CONFIRM to buy this stock at this price. If you do not want to make this purchase then simply do nothing. This will timeout in 30 seconds.")

                        # A really weird way to get multiple user replies
                        def stock_purchase_check(user_reply):

                            return user_reply.content.lower() == 'confirm' and message.author.id == user_reply.author.id

                        try:
                            user_reply = await client.wait_for('message', timeout=30.0, check=stock_purchase_check)

                        except asyncio.TimeoutError:
                            users_buying_stock.remove(message.author.id)

                            await message.channel.send("It appears you did not want to purchase any stock. The proposal has ended.")

                        else:
                            # If the user confirms they want the purchase
                            if user_reply.content.lower() == 'confirm':

                                # Takes the available stock and gives to the user, subtracts the money from their account

                                money -= (stock_value * int(split_message[3]) * 1.05)
                                db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                                available_stock -= int(split_message[3])
                                db_conn.execute("UPDATE Companies SET Available_Stocks = ? WHERE Company_Name = ?", (available_stock, company_name))

                                column_company_name = company_name.replace(' ', '_')

                                # This catches things like inserting the query 'Hand-Drawn Frames' as - breaks sqlite when searching column names
                                modified_column_company_name = column_company_name.replace('-', '_')

                                print(modified_column_company_name)

                                # Catches REMOVED FOR GITHUB_Co.'s period at the end
                                if modified_column_company_name[-1] == ".":
                                    modified_column_company_name = modified_column_company_name[:-1]

                                # Gets the user's current stock count for that company, adds it, then updates it within the database
                                users_current_stock = db_conn.execute("SELECT (%s) FROM Stocks WHERE User_ID = ?" % (modified_column_company_name),
                                                                      (message.author.id,))
                                users_current_stock = users_current_stock.fetchone()
                                users_current_stock = users_current_stock[0]

                                users_current_stock += int(split_message[3])

                                db_conn.execute("UPDATE Stocks SET (%s) = ? WHERE User_ID = ?" % (modified_column_company_name),
                                                (users_current_stock, message.author.id))

                                # Removes the person from the stock buying list
                                users_buying_stock.remove(message.author.id)

                                await message.channel.send("You successfully bought " + split_message[
                                    3] + " stock(s) from " + company_name + " at the total price of " + str(total_amount_due) + "$.")

                                # This will generate a general value to increase the worth of the company based on the stocks bought

                                # Market value luck, fluctuations, etc needs a huge overhaul!!!!!!!!!!!! ATTENTION HERE
                                market_influence = 0

                                print("Market influence is:", market_influence)

                                random_market_fluctuations = random.uniform(1.0, 2.0)

                                print("Random market fluctuations is:", random_market_fluctuations)

                                company_value_adjustment = total_amount_due * random_market_fluctuations

                                print("Company value increase is:", company_value_adjustment)

                                print(company_name)

                                # Updates and adds to the total company value based on the above factors
                                company_total_value = db_conn.execute('SELECT Total_Value FROM Companies WHERE Company_Name = ?', (company_name,))
                                company_total_value = company_total_value.fetchone()
                                company_total_value = company_total_value[0]

                                print(company_total_value)
                                company_total_value += round(company_value_adjustment, 2)

                                print(company_total_value)

                                db_conn.execute("UPDATE Companies SET Total_Value = ? WHERE Company_Name = ?", (company_total_value, company_name))

                                # Then we update the individual stock value to represent the new company's per-stock value
                                max_stock_count = db_conn.execute('SELECT Max_Stocks FROM Companies WHERE Company_Name = ?', (company_name,))
                                max_stock_count = max_stock_count.fetchone()
                                max_stock_count = max_stock_count[0]

                                stock_value = round(company_total_value / max_stock_count, 2)

                                print(stock_value)

                                db_conn.execute("UPDATE Companies SET Stock_Value = ? WHERE Company_Name = ?", (stock_value, company_name))

                                db_conn.commit()  # Make sure to commit this before doing any of the below logic

                                # Updates the user's Stock Value

                                # Fetches the user's total owned stock count and their total worth
                                stock_count = db_conn.execute("SELECT * FROM Stocks WHERE User_ID = " + str(message.author.id))
                                stock_count = stock_count.fetchone()

                                # Removes the first 3 elements of the generated list
                                stock_count = stock_count[3:]

                                # Gets all the stock
                                companies = db_conn.execute('SELECT * FROM Companies')
                                companies = companies.fetchall()

                                # Loops through the list of companies/stock and adds them together as it goes
                                total_stock_value = 0
                                loop_count = 0

                                for x in stock_count:
                                    total_stock_value += stock_count[loop_count] * companies[loop_count][5]

                                    loop_count += 1

                                db_conn.execute("UPDATE Members SET Stock_Value = " + str(round(total_stock_value, 2)) + " WHERE User_ID = " + str(
                                    message.author.id))
                                db_conn.commit()

                                # Updates the user's Net Worth
                                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                                money = money.fetchone()

                                bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(message.author.id))
                                bank = bank.fetchone()

                                stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(message.author.id))
                                stock_value = stock_value.fetchone()

                                net_worth = money[0] + bank[0] + stock_value[0]

                                db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(message.author.id))
                                db_conn.commit()

                                # We buff the company (if it hasn't been buffed yet today)
                                company_buff = db_conn.execute("SELECT Daily_Influence FROM Companies WHERE Company_Name = ?", (company_name,))
                                company_buff = company_buff.fetchone()
                                company_buff = company_buff[0]

                                market_trend = db_conn.execute("SELECT Market_Trend FROM Companies WHERE Company_Name = ?", (company_name,))
                                market_trend = market_trend.fetchone()
                                market_trend = market_trend[0]

                                # Checks if the company has been affected/influenced today by being bought or sold
                                if company_buff == 'Upward':
                                    print("Company has already been buffed today")

                                elif company_buff == 'Downward':
                                    print("Company has already been debuffed today")

                                    # 50% chance of actually affecting the market trend
                                    random_num = random.randint(1, 2)
                                    if random_num == 1:
                                        print("Pushing market trend back up")
                                        market_trend += 1

                                    else:
                                        print("Not pushing market trend back up")

                                    db_conn.execute("UPDATE Companies SET Daily_Influence = ? WHERE Company_Name = ?", ('None', company_name,))

                                    db_conn.execute("UPDATE Companies SET Market_Trend = ? WHERE Company_Name = ?", (market_trend, company_name))
                                    db_conn.commit()

                                else:
                                    print("Company has not been influenced today yet, pushing it upward")

                                    # 50% chance of actually affecting the market trend
                                    random_num = random.randint(1, 2)
                                    if random_num == 1:
                                        print("Pushing market trend up")
                                        market_trend += 1

                                    else:
                                        print("Not pushing market trend up")

                                    db_conn.execute("UPDATE Companies SET Daily_Influence = ? WHERE Company_Name = ?", ('Upward', company_name,))

                                    db_conn.execute("UPDATE Companies SET Market_Trend = ? WHERE Company_Name = ?", (market_trend, company_name))
                                    db_conn.commit()

                                # Adds a KP point to the user (if applicable)
                                stocks_bought = db_conn.execute(f"SELECT Stocks_Bought FROM Members WHERE User_ID = {message.author.id}")
                                stocks_bought = stocks_bought.fetchone()
                                stocks_bought = stocks_bought[0]

                                # Checks if the user has bought stocks today yet
                                if stocks_bought == 'None':

                                    db_conn.execute("UPDATE Members SET Stocks_Bought = ? WHERE User_ID = ?", ('Bought', message.author.id))
                                    db_conn.commit()

                                    db_conn.execute("UPDATE Members SET KP = KP + ? WHERE User_ID = ?", (1, message.author.id))
                                    db_conn.commit()












    if split_message[1] == 'sell':

        # Checks if the person is already trying to buy/sell stocks to prevent stock spam
        if message.author.id in users_buying_stock:
            await message.channel.send("You're already in the process of buying/selling stocks. Finish that first.")

        else:
            # Checks if the user is trying to sell less than 1 stock
            if int(split_message[3]) < 1:
                await message.channel.send("You need to sell at least 1 stock, my dude.")

            else:

                # First checks if the user even has enough of this specific stock
                company_name = stock_companies[split_message[2]]

                column_company_name = company_name.replace(' ', '_')

                # This catches things like inserting the query 'Hand-Drawn Frames' as - breaks sqlite when searching column names
                modified_column_company_name = column_company_name.replace('-', '_')

                print(modified_column_company_name)

                # Catches REMOVED FOR GITHUB_Co.'s period at the end
                if modified_column_company_name[-1] == ".":
                    modified_column_company_name = modified_column_company_name[:-1]

                # Gets the user's current stock count for that company
                users_current_stock = db_conn.execute("SELECT (%s) FROM Stocks WHERE User_ID = ?" % (modified_column_company_name), (message.author.id,))
                users_current_stock = users_current_stock.fetchone()
                users_current_stock = users_current_stock[0]

                # Checks if the user is trying to sell more stock than what they have
                if users_current_stock < int(split_message[3]):
                    await message.channel.send("You're trying to sell more stock than what you have!")

                else:
                    # Once all above checks have been met, we place the user into the buying_stocks list
                    users_buying_stock.append(message.author.id)

                    # Gets the current stock value
                    stock_value = db_conn.execute('SELECT Stock_Value FROM Companies WHERE Company_Name = ?', (company_name,))
                    stock_value = stock_value.fetchone()
                    stock_value = float(stock_value[0])

                    # Some math to get tax and total sell price
                    user_payment_amount = stock_value * int(split_message[3])
                    tax_amount = round(user_payment_amount * 0.05, 2)
                    total_amount_due = user_payment_amount - tax_amount

                    # Prompts the user for how much they'll be selling for, and asks for them to confirm
                    bot_message = await message.channel.send("You're attempting to sell " + split_message[3] + " stock(s) of the company " + stock_companies[split_message[2]] + ". " +
                        "Each stock has a value of " + str(stock_value) + "$, totalling your request stock value out to " + str(round(user_payment_amount, 2)) + "$ with a 5% tax (" + str(tax_amount) + "$), equaling a total of " + str(round(total_amount_due, 2)) + "$ due for sale." +
                        "\nPlease type CONFIRM to sell this stock at this price. If you do not want to make this sale then simply do nothing. This will timeout in 30 seconds.")

                    # A really weird way to get multiple user replies
                    def stock_sell_check(user_reply):

                        return user_reply.content.lower() == 'confirm' and message.author.id == user_reply.author.id

                    try:
                        user_reply = await client.wait_for('message', timeout=30.0, check=stock_sell_check)

                    except asyncio.TimeoutError:
                        users_buying_stock.remove(message.author.id)

                        await message.channel.send("It appears you did not want to sell any stock. The proposal has ended.")

                    else:
                        # If the user confirms the sale
                        if user_reply.content.lower() == 'confirm':

                            # Takes the available stock from the user
                            new_stock_count = users_current_stock - int(split_message[3])
                            db_conn.execute("UPDATE Stocks SET (%s) = ? WHERE User_ID = ?" % (modified_column_company_name), (new_stock_count, message.author.id))

                            # Gets the current money and adds the sale money to the user's account
                            money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                            money = money.fetchone()
                            money = float(money[0])

                            total_amount_due = round(total_amount_due, 2)

                            money += total_amount_due

                            db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                            # Gets the relevant company's stock count and adds the sold stock to it
                            available_stock = db_conn.execute('SELECT Available_Stocks FROM Companies WHERE Company_Name = ?', (company_name,))
                            available_stock = available_stock.fetchone()
                            available_stock = float(available_stock[0])

                            new_available_stock = available_stock + int(split_message[3])

                            db_conn.execute("UPDATE Companies SET Available_Stocks = ? WHERE Company_Name = ?", (new_available_stock, company_name))

                            # Removes the person from the stock buying list
                            users_buying_stock.remove(message.author.id)

                            await message.channel.send("You successfully sold " + split_message[3] + " stock(s) from " + company_name + " at the total income of " + str(total_amount_due) + "$.")

                            # This will generate a general value to increase the worth of the company based on the stocks bought

                            # Market value luck, fluctuations, etc needs a huge overhaul!!!!!!!!!!!! ATTENTION HERE
                            market_influence = 0

                            print("Market influence is:", market_influence)

                            random_market_fluctuations = random.uniform(0.5, 1.0)

                            print("Random market fluctations is:", random_market_fluctuations)

                            company_value_adjustment = total_amount_due * random_market_fluctuations

                            print("Company value increase is:", company_value_adjustment)

                            print(company_name)

                            # Updates and subtracts from the total company value based on the above factors
                            company_total_value = db_conn.execute('SELECT Total_Value FROM Companies WHERE Company_Name = ?', (company_name,))
                            company_total_value = company_total_value.fetchone()
                            company_total_value = company_total_value[0]

                            print(company_total_value)
                            company_total_value -= round(company_value_adjustment, 2)

                            print(company_total_value)

                            db_conn.execute("UPDATE Companies SET Total_Value = ? WHERE Company_Name = ?", (company_total_value, company_name))

                            # Then we update the individual stock value to represent the new company's per-stock value
                            max_stock_count = db_conn.execute('SELECT Max_Stocks FROM Companies WHERE Company_Name = ?', (company_name,))
                            max_stock_count = max_stock_count.fetchone()
                            max_stock_count = max_stock_count[0]

                            stock_value = round(company_total_value / max_stock_count, 2)

                            print(stock_value)

                            db_conn.execute("UPDATE Companies SET Stock_Value = ? WHERE Company_Name = ?", (stock_value, company_name))

                            db_conn.commit() # Make sure to commit this before doing any of the below logic

                            # Updates the user's Stock Value

                            # Fetches the user's total owned stock count and their total worth
                            stock_count = db_conn.execute("SELECT * FROM Stocks WHERE User_ID = " + str(message.author.id))
                            stock_count = stock_count.fetchone()

                            # Removes the first 3 elements of the generated list
                            stock_count = stock_count[3:]

                            # Gets all the stock
                            companies = db_conn.execute('SELECT * FROM Companies')
                            companies = companies.fetchall()

                            # Loops through the list of companies/stock and adds them together as it goes
                            total_stock_value = 0
                            loop_count = 0

                            for x in stock_count:
                                total_stock_value += stock_count[loop_count] * companies[loop_count][5]

                                loop_count += 1

                            db_conn.execute("UPDATE Members SET Stock_Value = " + str(round(total_stock_value, 2)) + " WHERE User_ID = " + str(message.author.id))
                            db_conn.commit()


                            # Updates the user's Net Worth
                            money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                            money = money.fetchone()

                            bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(message.author.id))
                            bank = bank.fetchone()

                            stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(message.author.id))
                            stock_value = stock_value.fetchone()

                            net_worth = money[0] + bank[0] + stock_value[0]

                            db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(message.author.id))
                            db_conn.commit()


                            # We de-buff the company (if it hasn't been de-buffed yet today)
                            company_buff = db_conn.execute("SELECT Daily_Influence FROM Companies WHERE Company_Name = ?", (company_name,))
                            company_buff = company_buff.fetchone()
                            company_buff = company_buff[0]

                            market_trend = db_conn.execute("SELECT Market_Trend FROM Companies WHERE Company_Name = ?", (company_name,))
                            market_trend = market_trend.fetchone()
                            market_trend = market_trend[0]

                            # Checks if the company has been affected/influenced today by being bought or sold
                            if company_buff == 'Downward':
                                print("Company has already been debuffed today")

                            elif company_buff == 'Upward':
                                print("Company has already been buffed today")

                                # 50% chance of actually affecting the market trend
                                random_num = random.randint(1, 2)
                                if random_num == 1:
                                    print("Pushing market trend back down")
                                    market_trend -= 1

                                else:
                                    print("Not pushing market trend back down")

                                db_conn.execute("UPDATE Companies SET Daily_Influence = ? WHERE Company_Name = ?", ('None', company_name,))

                                db_conn.execute("UPDATE Companies SET Market_Trend = ? WHERE Company_Name = ?", (market_trend, company_name))
                                db_conn.commit()

                            else:
                                print("Company has not been influenced today yet, pushing it downward")

                                # 50% chance of actually affecting the market trend
                                random_num = random.randint(1, 2)
                                if random_num == 1:
                                    print("Pushing market trend down")
                                    market_trend -= 1

                                else:
                                    print("Not pushing market trend down")

                                db_conn.execute("UPDATE Companies SET Daily_Influence = ? WHERE Company_Name = ?", ('Downward', company_name,))

                                db_conn.execute("UPDATE Companies SET Market_Trend = ? WHERE Company_Name = ?", (market_trend, company_name))
                                db_conn.commit()

                                # Adds a KP point to the user (if applicable)
                                stocks_bought = db_conn.execute(f"SELECT Stocks_Bought FROM Members WHERE User_ID = {message.author.id}")
                                stocks_bought = stocks_bought.fetchone()
                                stocks_bought = stocks_bought[0]

                                # Checks if the user has bought stocks today yet
                                if stocks_bought == 'None':

                                    db_conn.execute("UPDATE Members SET Stocks_Bought = ? WHERE User_ID = ?", ('Bought', message.author.id))
                                    db_conn.commit()

                                    db_conn.execute("UPDATE Members SET KP = KP + ? WHERE User_ID = ?", (1, message.author.id))
                                    db_conn.commit()