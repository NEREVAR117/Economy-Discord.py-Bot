












async def Top(db_conn, message):

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

        top_members_post += member[
                                1] + "'s net worth: " + net_worth + "$.  [Money: " + money + "$]  [Bank: " + bank + "$]  [Stocks: " + stock_value + "$]\n"

    top_members_post += '```'

    await message.channel.send(top_members_post)












async def Profile(message, db_conn, discord):
    # First check if the user is just doing -profile or -profile irl_name
    split_message = message.content.split()

    # Triggers if they're just checking their own profile
    if len(split_message) == 1:
        chosen_id = str(message.author.id)

        avatar = message.author.avatar_url_as(static_format="png")

    # Triggers if they're calling for another person's irl name
    else:
        ##### Old code that got user IDs and required users to use -money @user

        # Gets the proper ID number of the called user
        #chosen_id = split_message[1]
        #chosen_id = chosen_id[2:]
        #chosen_id = chosen_id[:-1]

        # Checks if a user's name in the server is different from the main account name (which adds an !)
        #if chosen_id[0] == '!':
            #chosen_id = chosen_id[1:]

        #called_user = message.guild.get_member(int(chosen_id))
        #avatar = called_user.avatar_url_as(static_format="png")


        # Gets the called irl name, capitalizes it, and gets their user ID
        irl_name = split_message[1]
        irl_name = irl_name.capitalize()

        chosen_id = db_conn.execute("SELECT User_ID FROM Members WHERE Nickname = ?", (irl_name,))
        chosen_id = chosen_id.fetchone()
        chosen_id = str(chosen_id[0])

        # Gets their avatar using their ID
        called_user = message.guild.get_member(int(chosen_id))
        avatar = called_user.avatar_url_as(static_format="png")



    # Checks if the person being profiled is even in the database
    check_if_user_is_present = db_conn.execute("SELECT User_ID FROM Members WHERE User_ID = " + chosen_id)
    check_if_user_is_present = check_if_user_is_present.fetchone()

    # Conditional statement to check if the person calling the prompt is even in the database
    if check_if_user_is_present == None and message.author.id == chosen_id:
        await message.channel.send("You need to type `-join` first if you want to join the economy.")

    # Triggers if they tried checking someone else not in the database
    elif check_if_user_is_present == None and message.author.id != chosen_id:
        await message.channel.send("Sadly, this person isn't part of our beautiful economy.")

    else:
        # Fetches the money of the profiled person
        member_data = db_conn.execute("SELECT * FROM Members WHERE User_ID = " + chosen_id)
        member_data = member_data.fetchone()

        # Fetches the user's total owned stock count and their total worth
        stock_count = db_conn.execute("SELECT * FROM Stocks WHERE User_ID = " + chosen_id)
        stock_count = stock_count.fetchone()

        # Fetches the user's KP points
        REMOVED FOR GITHUB_points = db_conn.execute('SELECT KP FROM Members WHERE User_ID = ?', (chosen_id,))
        REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points.fetchone()
        REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points[0]

        # Removes the first 3 elements of the generated list
        stock_count = stock_count[3:]

        # Gets all the stock
        companies = db_conn.execute('SELECT * FROM Companies')
        companies = companies.fetchall()

        # Loops through the list of companies/stock and adds them together as it goes
        total_stock_value = 0
        loop_count = 0

        for stock in stock_count:
            total_stock_value += stock_count[loop_count] * companies[loop_count][5]

            loop_count += 1

        # Compiles the footer for the embed below where all the companies and their individual stocks are owned by the user requested
        footer = ''
        loop_count = 0
        for company in companies:
            footer += company[0] + ": " + str(stock_count[loop_count]) + " | "

            loop_count += 1

        # Removes the excess | at the end of the string
        footer = footer[:-3]

        # Cleans up any float rounding issues
        net_worth = "%.2f" % round(member_data[3], 2)
        money = "%.2f" % round(member_data[4], 2)
        bank = "%.2f" % round(member_data[5], 2)
        stocks = "%.2f" % round(member_data[6], 2)

        # Begins creating the embed object
        # avatar = message.author.avatar_url_as(static_format="png")
        embed = discord.Embed(title="Stockmaster " + member_data[2], description="Net Worth: " + net_worth + "$   |   Stocks Owned: " + str(sum(stock_count)) + "   |   KP: " + str(REMOVED FOR GITHUB_points), color=0x21ebe6)
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Money", value=money + "$", inline=True)
        embed.add_field(name="Bank", value=bank + "$", inline=True)
        embed.add_field(name="Stocks", value=stocks + "$", inline=True)
        embed.set_footer(text=footer)

        await message.channel.send(embed=embed)


















async def Pay(message, time, db_conn):
    split_message = message.content.split()

    # Checks if the user did or did not input anything less than a penny (10.01 instead of something like 10.001)
    decimal_check = split_message[2]

    # This ensures a (textual) float is passed even if the user only uses an integer in their post
    if "." not in decimal_check:
        decimal_check = decimal_check + ".00"

    decimal_check = decimal_check.split(".")
    decimal_check = decimal_check[1]

    if len(decimal_check) > 2:
        await message.channel.send("You can't pay someone less than a penny, you buffoon.")

    else:

        ### Older method to get the Id required -pay @user but we're now using -pay irl_name
        # Gets the proper ID number
        #paid_user_id = split_message[1]
        #paid_user_id = paid_user_id[2:]
        #paid_user_id = paid_user_id[:-1]

        # Checks if a user's name in the server is different from the main account name (which adds an !)
        #if paid_user_id[0] == '!':
        #    paid_user_id = paid_user_id[1:]

        # Gets the called irl name, capitalizes it, and gets their user ID
        irl_name = split_message[1]
        irl_name = irl_name.capitalize()

        paid_user_id = db_conn.execute("SELECT User_ID FROM Members WHERE Nickname = ?", (irl_name,))
        paid_user_id = paid_user_id.fetchone()
        paid_user_id = str(paid_user_id[0])

        # Catches if the person is trying to pay themself
        if message.author.id == int(paid_user_id):
            await message.channel.send(
                "You slowly remove the money from your wallet. You place it on a nearby table. After a few moments you pocket the money.")
            time.sleep(3)
            await message.channel.send("Well done.")

        else:
            # Checks if the person being paid is even in the database
            check_if_user_is_present = db_conn.execute("SELECT User_ID FROM Members WHERE User_ID = " + paid_user_id)
            check_if_user_is_present = check_if_user_is_present.fetchone()

            # Conditional statement to check if the member is in the database or not
            if check_if_user_is_present == None:
                await message.channel.send("Sadly, this person is not participating in our glorious economy. The best economy. :thumbsup:")

            else:
                # Checks if the paying user even has enough money
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                money = money.fetchone()
                money = float(money[0])

                if money < float(split_message[2]):
                    await message.channel.send("Breaking the economy won't be that easy. You don't have enough cash. :no_entry_sign:")

                else:
                    # Subtracts from the paying user the money they declared
                    money = money - float(split_message[2])

                    print("Line 380, Money is:", money)

                    db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
                    db_conn.commit()

                    # Updates the paying user's Net Worth
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                    money = money.fetchone()

                    bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(message.author.id))
                    bank = bank.fetchone()

                    stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(message.author.id))
                    stock_value = stock_value.fetchone()

                    net_worth = money[0] + bank[0] + stock_value[0]

                    db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(message.author.id))
                    db_conn.commit()

                    # Gives to the paid user the money that is declared
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + paid_user_id)
                    money = money.fetchone()
                    money = float(money[0])

                    money = money + float(split_message[2])

                    print("Line 392, Money is:", money)

                    db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, paid_user_id))
                    db_conn.commit()

                    # Updates the paid user's Net Worth
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(paid_user_id))
                    money = money.fetchone()

                    bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(paid_user_id))
                    bank = bank.fetchone()

                    stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(paid_user_id))
                    stock_value = stock_value.fetchone()

                    net_worth = money[0] + bank[0] + stock_value[0]

                    db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(paid_user_id))
                    db_conn.commit()

                    await message.channel.send("You have successfully paid this person.")