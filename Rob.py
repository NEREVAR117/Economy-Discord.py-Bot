


async def RobPrompt(message):
    await message.channel.send('''```   The available rob commands are:
            -rob #user         (this tries to rob the mentioned user, generally for public use)
            -rob (irl name)    (tries to rob the named user, generally for private use)

    Robbing a player is suggested to be done privately so people don't know you're doing it. Private message the bot the command above.(```''')







async def Rob(message, db_conn, time, random, client):
    # Initial check to see if they still have to wait before robbing again

    # Fetches the time (in universal time) from the database so we know when the user last did -jobs
    last_rob_time = db_conn.execute("SELECT Last_Rob_Time FROM Members WHERE User_ID = " + str(message.author.id))
    last_rob_time = last_rob_time.fetchone()

    # Formatting the current time and subtracting last_job_time from it to get how many seconds it's been since they did a job
    replacement_job_time = time.time()
    replacement_job_time = round(replacement_job_time)

    last_rob_time = replacement_job_time - last_rob_time[0]

    print("It's been", last_rob_time, "seconds since they tried robbing someone")

    # This checks if it's been 172,800 seconds (2 days) since they last completed a job
    if last_rob_time < 172800:

        remainder = 172800 - last_rob_time

        # Janky way to get time left for the user (longer than one day / 24 hours)
        day = remainder // (24 * 3600)
        remainder = remainder % (24 * 3600)
        hour = remainder // 3600
        remainder %= 3600
        minutes = remainder // 60
        remainder %= 60
        seconds = remainder

        await message.channel.send(f"You should wait {day} day(s), {hour} hour(s), {minutes} minute(s), and {seconds} second(s) before robbing again. It's too risky to do it so soon. :ninja:")

    else:
        # Split the message if the user is allowed to rob
        split_message = message.content.split()

        user_called = split_message[1]
        user_called = user_called.capitalize()

        print(user_called)

        # First checks if they're calling @user or a real life name
        if split_message[1][1] != '@':
            print("derp")
            getting_robbed_id = db_conn.execute('SELECT User_ID FROM Members WHERE Nickname = ?', (user_called,))
            print(getting_robbed_id)
            getting_robbed_id = getting_robbed_id.fetchone()
            print(getting_robbed_id)
            getting_robbed_id = getting_robbed_id[0]

        else:
            # Gets the proper ID number of the called user
            getting_robbed_id = split_message[1]
            getting_robbed_id = getting_robbed_id[2:]
            getting_robbed_id = getting_robbed_id[:-1]

            # Checks if a user's name in the server is different from the main account name (which adds an !)
            if getting_robbed_id[0] == '!':
                getting_robbed_id = getting_robbed_id[1:]

        print(getting_robbed_id)
        print(message.author.id)

        # Second we check if the person is trying to rob themself
        if getting_robbed_id == message.author.id:
            await message.channel.send("You hold a weapon up to yourself and threaten to give yourself your own money. You're an idiot.")

        else:
            # If robbing someone else, check if the robber user has a gun
            gun_check = db_conn.execute('SELECT Gun FROM Inventory WHERE User_ID = ?', (message.author.id,))
            gun_check = gun_check.fetchone()
            gun_check = gun_check[0]

            print(gun_check)

            robbery_success_chance = 30

            if gun_check == 'Owned':
                robbery_success_chance += 30

            # Add a chance mask modifier here for succeeding

            # Also add one for night time robberies

            # Secondly, checks the robbed person's inventory
            robbed_members = db_conn.execute('SELECT * FROM Inventory WHERE User_ID = ?', (getting_robbed_id,))
            robbed_members = robbed_members.fetchall()
            robbed_members = robbed_members[0]

            print(robbed_members)

            if robbed_members[3] == 'Owned':
                print("Person being robbed has a Kirby")
                robbery_success_chance -= 5

            if robbed_members[5] == 'Owned':
                print("Person being robbed has a gun")
                robbery_success_chance -= 25

            if robbed_members[6] == 'Owned':
                print("Person being robbed has a suit")
                robbery_success_chance += 15

            if robbed_members[7] == 'Owned':
                print("Person being robbed has a car")
                robbery_success_chance -= 15

            print("Robbery success chance is:", robbery_success_chance)

            # Always gives the robber some chance to succeed
            if robbery_success_chance <= 0:
                print("Robbery success chance was too low (less than 0%) so it's been set to 5%")
                robbery_success_chance = 5

            money_dropped = False
            spotted = False

            # Rolls and checks if the robbery succeeds
            roll_chance = random.randint(1, 100)

            print("Robbery roll chance:", roll_chance)
            print("Robbery success chance:", robbery_success_chance)

            # Catches if not triggered below
            money_stolen = 0
            dropped_money = 0

            if roll_chance > robbery_success_chance:
                print("Robbery failed")

                robbery_success = False

            else:
                print("Robbery succeeded")

                robbery_success = True

                # Gets the robbed user's money and updates the money stolen
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = ?", (getting_robbed_id,))
                money = money.fetchone()
                money = money[0]

                money_stolen_percentage = random.uniform(0.1, 0.6)  # 10% to 60%

                money_stolen = money * money_stolen_percentage

                # Triggers so not -too much- money is ever stolen at once
                if money_stolen > 500:
                    money_stolen = 500

                    money_stolen_percentage = random.uniform(0.9, 0.97)  # 90% to 97%

                    print(money_stolen_percentage)

                    money_stolen = money_stolen * money_stolen_percentage

                print("Money stolen is", money_stolen)

                money -= money_stolen

                money = float("%.2f" % round(money, 2))

                print("The person being robbed lost", money_stolen, "dollars")

                db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, getting_robbed_id))
                db_conn.commit()

                # Now adds the stolen money to the robber
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = ?", (message.author.id,))
                money = money.fetchone()
                money = money[0]

                # Small chance of some of the money being dropped when stolen
                drop_chance = random.randint(1, 100)

                if 1 == 1 or (drop_chance <= 33 and money_stolen >= 5):  # 1 in 3 chance of losing some money if over 5$

                    money_dropped = True

                    print("Robber dropped some money")

                    dropped_money_percentage = random.uniform(0.6, 0.90)  # 60% to 90%

                    dropped_money = money_stolen * dropped_money_percentage
                    dropped_money = money_stolen - dropped_money
                    dropped_money = float("%.2f" % round(dropped_money, 2))

                    money_stolen = money_stolen * dropped_money_percentage

                money_stolen = float("%.2f" % round(money_stolen, 2))

                print("Robber gained", money_stolen, "dollars")

                money += money_stolen

                money = float("%.2f" % round(money, 2))

                db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
                db_conn.commit()

            # Checks if the user was spotted or not
            spotted_chance = random.randint(1, 100)
            # Add a mask chance modifier here for someone being spotted
            # Same for it being night time or not

            print("Spotted chance is", spotted_chance)
            if spotted_chance <= 33:  # 1 in 3 chance of the robber being spotted
                print("The robber was spotted!")

                spotted = True

            # Recreates the total taken from the robbed person
            robbed_money_lost = money_stolen + dropped_money
            robbed_money_lost = float("%.2f" % round(robbed_money_lost, 2))

            # Now, finally, checks if this was sent from a DM or not. Very important. Then sends all the messages
            if message.guild == None:
                print("This robbery was done via DMs")

                # Gets the robber's irl name to send the robbed user
                irl_name = db_conn.execute("SELECT Username FROM Members WHERE User_ID = ?", (message.author.id,))
                irl_name = irl_name.fetchone()
                irl_name = irl_name[0]

                robbed_user = client.get_user(getting_robbed_id)

                await message.channel.send("You head out and begin looking for a target to steal from. You finally spot someone...")

                # Small delay while the robbery happens...
                time.sleep(3)

                if robbery_success == True:

                    if spotted == True:

                        if money_dropped == True:
                            print("Debug message farpa")
                            await message.channel.send(
                                f"You managed to steal {robbed_money_lost}$ from {user_called} and get away, dropping {dropped_money}$ as you fled the scene. However... your identity was seen.")


                        else:
                            print("Debug message reeeee")
                            await message.channel.send(
                                f"You managed to steal {robbed_money_lost}$ from {user_called} and get away. However... your identity was seen.")

                        print("Debug message mmmmmm")
                        # Sends to the robbed user only if robber spotted
                        await robbed_user.send(
                            f"Suddenly, {irl_name} appears and manages to take you by surprise, and they steal {robbed_money_lost}$ from you. Can't trust anyone.")


                    else:
                        if money_dropped == True:
                            print("Debug message olololol")
                            await message.channel.send(
                                f"You managed to steal {robbed_money_lost}$ from {user_called} and get away unseen, dropping {dropped_money}$ as you fled the scene.")

                        else:
                            print("Debug message aawawaw")
                            await message.channel.send(f"You managed to steal {robbed_money_lost}$ from {user_called} and get away unseen.")

                        # Sends to the robbed user only if robber is NOT spotted
                        print("Debug message blargh")
                        await robbed_user.send(
                            f"Suddenly, an unknown persons appears and manages to take you by surprise, and they steal {robbed_money_lost}$ from you. That sucks.")


                # Robbery failed
                else:
                    if spotted == True:
                        print("Debug message 1111111")
                        await message.channel.send("Unfortunately for you the robbery failed. You managed to get away... but your identity was seen.")
                        # Sends to the robbed user only if robber spotted
                        await robbed_user.send(
                            f"Suddenly, {irl_name} appears and manages to take you by surprise, but you manage to keep them from stealing from you. Can't trust anyone.")

                    else:
                        print("Debug message derka")
                        await message.channel.send("Unfortunately for you the robbery failed. However you managed to get away unseen.")
                        # Sends to the robbed user only if robber is NOT spotted
                        await robbed_user.send(
                            f"Suddenly, an unknown person appears and manages to take you by surprise, but you manage to keep them from stealing from you.")






            # Public robbing done
            else:
                print("This robbery was done publicly")

                # Get's the person's server name if called like -rob @user
                robbed_name = db_conn.execute('SELECT Username FROM Members WHERE User_ID = ?', (getting_robbed_id,))
                robbed_name = robbed_name.fetchone()
                robbed_name = robbed_name[0]

                await message.channel.send("You head out and begin looking for a target to steal from. You finally spot someone...")

                # Small delay while the robbery happens...
                time.sleep(3)

                if robbery_success == True:

                    if money_dropped == True:
                        await message.channel.send(
                            f"You managed to steal {robbed_money_lost}$ from {robbed_name} and get away, dropping {dropped_money}$ as you fled the scene. However... your identity was obviously seen.")

                    else:
                        await message.channel.send(
                            f"You managed to steal {robbed_money_lost}$ from {robbed_name} and get away. However... your identity was obviously seen.")


                # Robbery failed
                else:
                    await message.channel.send(
                        "Unfortunately for you the robbery failed. You managed to get away. However... your identity was obviously seen.")

            # Saves when the user robbed so they have to wait before -rob again
            unix_time = str(time.time())

            unix_time = unix_time.split(".")
            unix_time = unix_time[0]

            print(unix_time)

            db_conn.execute("UPDATE Members SET Last_Rob_Time = ? WHERE User_ID = ?", (unix_time, message.author.id))
            db_conn.commit()

            # Updates the networth of the robber and the robbed
            if robbery_success == True:
                # Updates the robber's Net Worth
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                money = money.fetchone()

                bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(message.author.id))
                bank = bank.fetchone()

                stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(message.author.id))
                stock_value = stock_value.fetchone()

                net_worth = money[0] + bank[0] + stock_value[0]

                db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(message.author.id))
                db_conn.commit()

                # Updates the robber user's Net Worth
                money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(getting_robbed_id))
                money = money.fetchone()

                bank = db_conn.execute("SELECT Bank FROM Members WHERE User_ID = " + str(getting_robbed_id))
                bank = bank.fetchone()

                stock_value = db_conn.execute("SELECT Stock_Value FROM Members WHERE User_ID = " + str(getting_robbed_id))
                stock_value = stock_value.fetchone()

                net_worth = money[0] + bank[0] + stock_value[0]

                db_conn.execute("UPDATE Members SET Net_Worth = " + str(round(net_worth, 2)) + " WHERE User_ID = " + str(getting_robbed_id))
                db_conn.commit()

                print("Updated both the robber's and robbed user's net worths")


            # Adds a KP point to the robber
            db_conn.execute('UPDATE Members SET KP = KP + 1 WHERE User_ID = ?', (message.author.id,))
            db_conn.commit()