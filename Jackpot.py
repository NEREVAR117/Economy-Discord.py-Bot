


async def JackpotPrompt(message, db_conn):
    # Gets the jackpot sum total to print to the user below
    jackpot_sum = db_conn.execute("SELECT SUM(Jackpot_Amount) FROM Members")
    jackpot_sum = jackpot_sum.fetchone()
    jackpot_sum = jackpot_sum[0]

    # Gets the total players in the jackpot right now
    temp_jackpot_check = db_conn.execute("SELECT Jackpot_Amount FROM Members WHERE Jackpot_Amount > 0.0")
    temp_jackpot_check = temp_jackpot_check.fetchall()

    player_count = len(temp_jackpot_check)

    # Formats the money amount properly (1.00 instead of just 1)
    jackpot_sum = "%.2f" % round(jackpot_sum, 2)

    # Fixes a divide by 0 issue, and responses with an accurate message depending if a jackpot is happening or not
    if player_count == 0:
        output_response = "There is currently no jackpot going. Do you want to start one?"

    else:
        # Formats the money amount properly (1.00 instead of just 1)
        temp_response = float(jackpot_sum) / player_count
        temp_response = "%.2f" % round(temp_response, 2)
        output_response = "The current jackpot amount is " + jackpot_sum + "$ and there are " + str(
            player_count) + " participant(s). To join you must pay " + temp_response + "$."

    await message.channel.send(
        "Type `-jackpot X` where X is the amount of money to either start or join an ongoing jackpot. Others will need to pay that same amount to join. It pays out at 9pm daily. \n" + output_response)







async def Jackpot(message, db_conn):
    split_message = message.content.split()

    # Retrieves the total amount of cash inside the jackpot
    jackpot_sum = db_conn.execute("SELECT SUM(Jackpot_Amount) FROM Members")
    jackpot_sum = jackpot_sum.fetchone()
    jackpot_sum = jackpot_sum[0]

    # Takes the string and tries to convert it into a float
    pay_in_amount = float(split_message[1])

    # If it's now a float, we continue into the main code
    if isinstance(pay_in_amount, float) == True:

        # Checks if the paying user even has enough money
        money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
        money = money.fetchone()
        money = float(money[0])

        if pay_in_amount > money:
            await message.channel.send("Sorry, friendo, but you're too broke for that.")

        # Checks to make sure the user is putting in at least a penny
        elif pay_in_amount < 0.01:
            await message.channel.send("You gotta pay at least a penny, my dude.")

        else:
            if jackpot_sum == 0.0:
                # Formats the money amount properly (1.00 instead of just 1)
                pay_in_amount = float("%.2f" % round(pay_in_amount, 2))

                await message.channel.send("The jackpot is empty, so you're starting one at " + str(pay_in_amount) + "$.")

                # Subtracts from the jackpot user their chosen amount
                print(money)
                money = money - pay_in_amount
                print(money)

                db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
                db_conn.commit()

                # Add the user's chosen money amount to the jackpot.
                db_conn.execute("UPDATE Members SET Jackpot_Amount = ? WHERE User_ID = ?", (pay_in_amount, message.author.id))
                db_conn.commit()

                # Adds a KP point to the user
                REMOVED FOR GITHUB_point = db_conn.execute(f"SELECT KP FROM Members WHERE User_ID = {message.author.id}")
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point.fetchone()
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point[0]

                REMOVED FOR GITHUB_point += 1

                db_conn.execute(f"UPDATE Members SET KP = {REMOVED FOR GITHUB_point} WHERE User_ID = {message.author.id}")
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

            else:

                # Checks to see if they're even paying the proper amount of money (whatever was originally put in)
                temp_jackpot_check = db_conn.execute("SELECT Jackpot_Amount FROM Members WHERE Jackpot_Amount > 0.0")
                temp_jackpot_check = temp_jackpot_check.fetchone()
                temp_jackpot_check = temp_jackpot_check[0]

                if temp_jackpot_check != pay_in_amount:
                    await message.channel.send("You must pay the original amount chosen for the jackpot, which is " + str(temp_jackpot_check) + "$.")


                else:
                    # Checks to see if this person has already paid into this jackpot
                    temp_jackpot_check = db_conn.execute("SELECT Jackpot_Amount FROM Members WHERE User_ID = " + str(message.author.id))
                    temp_jackpot_check = temp_jackpot_check.fetchone()
                    temp_jackpot_check = temp_jackpot_check[0]

                    if temp_jackpot_check == 0.0:
                        await message.channel.send(
                            "A jackpot is already going. You throw in " + str(pay_in_amount) + "$. The total jackpot amount is now " + str(
                                jackpot_sum + pay_in_amount) + "$.")

                        print(money)
                        # Subtracts from the jackpot user their chosen amount
                        money = money - pay_in_amount
                        print(money)

                        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
                        db_conn.commit()

                        # Add the user's chosen money amount to the jackpot.
                        db_conn.execute("UPDATE Members SET Jackpot_Amount = ? WHERE User_ID = ?", (pay_in_amount, message.author.id))
                        db_conn.commit()

                        # Adds a KP point to the user
                        REMOVED FOR GITHUB_point = db_conn.execute(f"SELECT KP FROM Members WHERE User_ID = {message.author.id}")
                        REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point.fetchone()
                        REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point[0]

                        REMOVED FOR GITHUB_point += 1

                        db_conn.execute(f"UPDATE Members SET KP = {REMOVED FOR GITHUB_point} WHERE User_ID = {message.author.id}")
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


                    else:
                        await message.channel.send("You're already in the jackpot for today. Don't get greedy.")