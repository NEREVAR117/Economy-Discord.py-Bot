
# Old lottery payout rates

derp = 10

if derp == 20:
    # Established the chances for all the lottery types

    # Lottery 1 average payout = 0.85$ (85%)
    lottery_1_winnings = [*(33 * [0]), *(17 * [1]), *(7 * [2]), *(2 * [5]), *(1 * [10])]  # This is 85% payout

    # Lottery 5 average payout = 4.50$ (90%)
    lottery_5_winnings = [*(10 * [0]), *(8 * [1]), *(11 * [2]), *(15 * [5]), *(3 * [10]), *(2 * [20]), *(1 * [50])]  # This is 90% payout

    # Lottery 10 average payout = 9.50$ (95%)
    lottery_10_winnings = [*(5 * [0]), *(5 * [1]), *(9 * [2]), *(14 * [5]), *(14 * [10]), *(4 * [20]), *(2 * [50]), *(1 * [100])]  # This is 95% payout

    # Lottery 25 average payout = 25$ (100%)
    lottery_25_winnings = [*(1 * [0]), *(2 * [1]), *(4 * [2]), *(8 * [5]), *(11 * [10]), *(7 * [20]), *(12 * [25]), *(6 * [50]), *(2 * [100]), *(1 * [250])]  # This is 100% payout

    # Lottery 50 average payout = 52.5$ (105%)
    lottery_50_winnings = [*(1 * [0]), *(1 * [1]), *(2 * [2]), *(4 * [5]), *(5 * [10]), *(8 * [20]), *(10 * [25]), *(13 * [50]), *(7 * [100]), *(2 * [250]), *(1 * [500])]  # This is 105% payout

    # Lottery 100 average payout = 110$ (110%)
    lottery_100_winnings = [*(1 * [0]), *(1 * [1]), *(2 * [2]), *(3 * [5]), *(4 * [10]), *(5 * [20]), *(6 * [25]), *(11 * [50]), *(13 * [100]), *(6 * [250]), *(3 * [500]), *(1 * [1000])]  # This is 110% payout







async def LotteryPrompt(message):

    await message.channel.send("""Type `-lottery X` where X is the cost of the lottery ticket. Ticket prices are: 1$, 5$, 10$, 25$, 50$, and 100$. The more expensive the ticket, the higher the potential payout and better the chances of winning.""")






async def Lottery(message, db_conn, time, random):

    split_message = message.content.split()

    # Checks if the person buying the lottery ticket is even in the database
    check_if_user_is_present = db_conn.execute("SELECT User_ID FROM Members WHERE User_ID = " + str(message.author.id))
    check_if_user_is_present = check_if_user_is_present.fetchone()

    if check_if_user_is_present == None:
        await message.channel.send("You're not valid to purchase a lottery ticket. Try joining the economy via the `-join` command!")

    else:
        # Checks if the paying user even has enough money
        money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
        money = money.fetchone()
        money = float(money[0])

        if money < int(split_message[1]):
            await message.channel.send("You don't have enough money for that lottery ticket. Get out of here you bum!")

        else:
            # Checks if the user has bought their maximum lotteries for the day or not
            lottery_count = db_conn.execute("SELECT Lottery_Count FROM Members WHERE User_ID = " + str(message.author.id))
            lottery_count = lottery_count.fetchone()
            lottery_count = lottery_count[0]

            # This checks the Black Market inventory to see what upgrades the user has
            lottery_data = db_conn.execute("SELECT * FROM Black_Market WHERE User_ID = " + str(message.author.id))
            lottery_data = lottery_data.fetchone()

            # Default 1 ticket a day
            lottery_max = 1

            if lottery_data[14] == 'Owned':
                lottery_max = 2

            if lottery_data[15] == 'Owned':
                lottery_max = 3

            if lottery_data[16] == 'Owned':
                lottery_max = 4

            if lottery_data[17] == 'Owned':
                lottery_max = 5

            if lottery_data[18] == 'Owned':
                lottery_max = 6

            if lottery_data[19] == 'Owned':
                lottery_max = 7

            if lottery_data[20] == 'Owned':
                lottery_max = 8


            # Now we compare the two variables
            if lottery_count >= lottery_max:
                await message.channel.send("You've already bought your maximum lottery tickets for the day!")

            else:
                await message.channel.send("You hand over your money and retrieve your ticket. You open it to check what you won...")
                time.sleep(3)

                # Lottery 2 average payout = 1.6$ (80%) UNUSED NOW
                # lottery_2_winnings = [*(36 * [0]), *(19 * [1]), *(10 * [2]), *(3 * [5]), *(1 * [10]), *(1 * [20])] #This is 60% payout
                # lottery_2_winnings = [*(20 * [0]), *(15 * [1]), *(10 * [2]), *(3 * [5]), *(1 * [10]), *(1 * [20])] #This is 80# payout

                # Established the chances for all the lottery types

                # All have an average payout of 105% with 1 in 100 chance of 10x value gain
                lottery_1_winnings = [*(44 * [0]), *(30 * [1]), *(20 * [2]), *(5 * [5]), *(1 * [10])]  # Payout is 105% at 1.05$

                lottery_5_winnings = [*(19 * [0]), *(14 * [1]), *(18 * [2]), *(25 * [5]), *(16 * [10]), *(7 * [20]), *(1 * [50])]  # Payout is 105% at 5.25$

                lottery_10_winnings = [*(11 * [0]), *(7 * [1]), *(14 * [2]), *(19 * [5]), *(26 * [10]), *(18 * [20]), *(4 * [50]), *(1 * [100])]  # Payout is 105% at 10.50$

                lottery_25_winnings = [*(7 * [0]), *(4 * [1]), *(8 * [2]), *(14 * [5]), *(21 * [10]), *(23 * [25]), *(14 * [50]), *(8 * [100]), *(1 * [250])]  # Payout is 105% at 26.25$

                lottery_50_winnings = [*(1 * [0]), *(2 * [1]), *(4 * [2]), *(6 * [5]), *(11 * [10]), *(38 * [25]), *(22 * [50]), *(8 * [100]), *(7 * [250]), *(1 * [500])]  # Payout is 105% at 52.50$

                lottery_100_winnings = [*(0 * [0]), *(2 * [1]), *(4 * [2]), *(6 * [5]), *(8 * [10]), *(9 * [20]), *(10 * [25]), *(16 * [50]), *(29 * [100]), *(9 * [250]), *(6 * [500]), *(1 * [1000])]  # Payout is 105% at 105$

                # Defines the lottery logic as a function for re-use so we don't waste tons of spaces for slight variants
                async def lottery_function(money, lottery_count):
                    lottery_result = random.choice(lottery_x_winnings)

                    print("Lottery payout from " + message.author.display_name + " is:", lottery_result)

                    # Subtracts from the paying user the money they declared and adds their lottery winnings
                    money = money - float(split_message[1]) + lottery_result

                    db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
                    db_conn.commit()

                    # Iterates the user's lottery count by 1
                    lottery_count += 1

                    db_conn.execute("UPDATE Members SET Lottery_Count = ? WHERE User_ID = ?", (lottery_count, message.author.id))
                    db_conn.commit()

                    what_user_paid = int(split_message[1])

                    if lottery_result == 0:
                        await message.channel.send("Oof. You got 0$ from the ticket. Hopefully you didn't pay a lot!")

                    elif lottery_result < what_user_paid:
                        await message.channel.send("You only got " + str(lottery_result) + "$ from the ticket. Better luck next time.")

                    elif lottery_result == what_user_paid:
                        await message.channel.send("You won " + str(lottery_result) + "$ from the ticket. At least you broke even!")

                    elif lottery_result == (10 * what_user_paid):
                        await message.channel.send(
                            ":fireworks: You hit the jackpot!! :star_struck: " + str(lottery_result) + "$ from the ticket. Bet it won't happen gain.")

                    elif lottery_result > what_user_paid:
                        await message.channel.send("Congrats, you won " + str(lottery_result) + "$ from the ticket. Isn't that just neat.")

                    else:
                        print("There was an error. Whoops. :')")

                # This determines which lottery winnings list to pass into the function
                if message.content == ('-lottery 1'):
                    lottery_x_winnings = lottery_1_winnings

                if message.content == ('-lottery 5'):
                    lottery_x_winnings = lottery_5_winnings

                if message.content == ('-lottery 10'):
                    lottery_x_winnings = lottery_10_winnings

                if message.content == ('-lottery 25'):
                    lottery_x_winnings = lottery_25_winnings

                if message.content == ('-lottery 50'):
                    lottery_x_winnings = lottery_50_winnings

                if message.content == ('-lottery 100'):
                    lottery_x_winnings = lottery_100_winnings

                # Finally, it runs the lottery logic here at the end
                await lottery_function(money, lottery_count)

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