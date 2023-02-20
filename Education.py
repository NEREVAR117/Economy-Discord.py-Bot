





async def EducationPrompt(message):
    await message.channel.send("""Education commands are the following:
        ```-education info       (display education information)
    -education study      (you study for a day to work towards the next educational goal)```""")





async def Education(message, db_conn, client, asyncio):
    split_message = message.content.split()

    if split_message[1] == "info":
        await message.channel.send("""You can study once per day to work towards earning the next degree/educational goal.
    Each educational tier allows you to earn more money passively and from doing jobs. The tiers are:     
        [Days To Earn - Tuition Cost - Educational Tier]
        10 - 0$ - High School
        30 - 1,000$ - Associates
        50 - 10,000 - Bachelors
        70 - 50,000 - Masters
        90 - 100,000 - PHD""")

    if split_message[1] == "study":
        education_study = db_conn.execute("SELECT Education FROM Members WHERE User_ID = " + str(message.author.id))
        education_study = education_study.fetchone()
        education_study = education_study[0]

        # First checks if the user has done -education study today
        if '.day_wait' in education_study:
            await message.channel.send("You've already studied today. Try again tomorrow.")

        else:

            # Function so we don't clog up all the different study pathways below
            async def kp_points():
                # Adds a KP point to the user
                REMOVED FOR GITHUB_point = db_conn.execute(f"SELECT KP FROM Members WHERE User_ID = {message.author.id}")
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point.fetchone()
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point[0]

                print(REMOVED FOR GITHUB_point)

                REMOVED FOR GITHUB_point += 1

                print(REMOVED FOR GITHUB_point)

                db_conn.execute(f"UPDATE Members SET KP = {REMOVED FOR GITHUB_point} WHERE User_ID = {message.author.id}")
                db_conn.commit()

            # Logical pathways to determine what to do with the educational level

            # Pre high School
            if int(education_study) < 10:

                if int(education_study) == 0:

                    await message.channel.send("Unlike real life, this is your first step towards a brighter, better-paying future!"
                                               "\nYou are " + str(int(education_study) + 1) + "/10th done getting your high school degree.")

                else:
                    await message.channel.send(
                        "You spend several hours and much energy trying to avoid your work rather than just doing it, but you eventually manage to finish and turn it in." +
                        "\nYou are now " + str(int(education_study) + 1) + "/10th done getting your high school degree.")

                education_study = int(education_study) + 1
                education_study = str(education_study) + ".day_wait"

                db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                db_conn.commit()

                # Gives the user a KP point
                await kp_points()



            # Finished High School
            elif int(education_study) == 10:

                await message.channel.send("Lucky for you, and unlucky for the glorious tax payers, high school is free. Here's your diploma.")

                education_study = int(education_study) + 1
                education_study = str(education_study) + ".day_wait"

                db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                db_conn.commit()

                # Gives the user a KP point
                await kp_points()



            # Pre associates degree
            elif int(education_study) > 10 and int(education_study) < 30:

                await message.channel.send("Your nights are spent stressing over your studies and wondering if this is all worth the effort." +
                                           "\nYou are now " + str(int(education_study) - 10) + "/20th done getting your associates degree.")

                education_study = int(education_study) + 1
                education_study = str(education_study) + ".day_wait"

                db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                db_conn.commit()

                # Gives the user a KP point
                await kp_points()



            # Finished associates degree
            elif int(education_study) == 30:

                # Prompts the user for how much they'll be spending, and asks for them to confirm
                bot_message = await message.channel.send(
                    "You've completed your studies for the associates degree. However you must pay 1,000$ to get it." +
                    "\nPlease type CONFIRM to pay 1,000$ for your associates degree. If you do not want to do this then simply do nothing. This will timeout in 30 seconds.")

                # A really weird way to get multiple user replies
                def stock_purchase_check(user_reply):

                    return user_reply.content.lower() == 'confirm' and message.author.id == user_reply.author.id

                try:
                    user_reply = await client.wait_for('message', timeout=30.0, check=stock_purchase_check)

                except asyncio.TimeoutError:

                    await message.channel.send("Guess you didn't want to move up in life. What a chump.")

                else:
                    # Checks if the user even has enough money
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                    money = money.fetchone()
                    money = float(money[0])

                    if money < 1000:
                        await message.channel.send("You don't even have enough money for your degree? Go bag some groceries.")

                    else:
                        # Deducts money from the user
                        money -= 1000

                        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                        # Gives the user their associates degree by incrementing Education further
                        education_study = int(education_study) + 1
                        education_study = str(education_study) + ".day_wait"

                        db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                        db_conn.commit()

                        # Gives the user a KP point
                        await kp_points()

                        await message.channel.send("Congrats. I guess. Here's your associates degree.")



            # Pre bachelors degree
            elif int(education_study) > 30 and int(education_study) < 50:

                await message.channel.send(
                    "You're still stressed about school, but not as much. You feel you're finally starting to get the groove of things." +
                    "\nYou are now " + str(int(education_study) - 30) + "/20th done getting your bachelors degree.")

                education_study = int(education_study) + 1
                education_study = str(education_study) + ".day_wait"

                db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                db_conn.commit()

                # Gives the user a KP point
                await kp_points()



            # Finished bachelors degree
            elif int(education_study) == 50:

                # Prompts the user for how much they'll be spending, and asks for them to confirm
                bot_message = await message.channel.send(
                    "You've completed your studies for the bachelors degree. However you must pay 10,000$ to get it." +
                    "\nPlease type CONFIRM to pay 10,000$ for your bachelors degree. If you do not want to do this then simply do nothing. This will timeout in 30 seconds.")

                # A really weird way to get multiple user replies
                def stock_purchase_check(user_reply):

                    return user_reply.content.lower() == 'confirm' and message.author.id == user_reply.author.id

                try:
                    user_reply = await client.wait_for('message', timeout=30.0, check=stock_purchase_check)

                except asyncio.TimeoutError:

                    await message.channel.send("What's wrong, 10k too much for you?")

                else:
                    # Checks if the user even has enough money
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                    money = money.fetchone()
                    money = float(money[0])

                    if money < 10000:
                        await message.channel.send("You don't even have enough money for your degree? Go clean some toilets.")

                    else:
                        # Deducts money from the user
                        money -= 10000

                        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                        # Gives the user their bachelors degree by incrementing Education further
                        education_study = int(education_study) + 1
                        education_study = str(education_study) + ".day_wait"

                        db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                        db_conn.commit()

                        # Gives the user a KP point
                        await kp_points()

                        await message.channel.send("So you earned a bachelors. Big Deal. Take it and go.")



            # Pre masters degree
            elif int(education_study) > 50 and int(education_study) < 70:

                await message.channel.send(
                    "You thought things would get easier. Nope, they got harder. Master's are difficult to earn. This sucks. School sucks." +
                    "\nYou are now " + str(int(education_study) - 50) + "/20th done getting your masters degree.")

                education_study = int(education_study) + 1
                education_study = str(education_study) + ".day_wait"

                db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                db_conn.commit()

                # Gives the user a KP point
                await kp_points()



            # Finished masters degree
            elif int(education_study) == 70:

                # Prompts the user for how much they'll be spending, and asks for them to confirm
                bot_message = await message.channel.send(
                    "You've completed your studies for the masters degree. However you must pay 50,000$ to get it." +
                    "\nPlease type CONFIRM to pay 50,000$ for your masters degree. If you do not want to do this then simply do nothing. This will timeout in 30 seconds.")

                # A really weird way to get multiple user replies
                def stock_purchase_check(user_reply):

                    return user_reply.content.lower() == 'confirm' and message.author.id == user_reply.author.id

                try:
                    user_reply = await client.wait_for('message', timeout=30.0, check=stock_purchase_check)

                except asyncio.TimeoutError:

                    await message.channel.send("Yeah, I don't blame you. 50,000$ is a lot of money.")

                else:
                    # Checks if the user even has enough money
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                    money = money.fetchone()
                    money = float(money[0])

                    if money < 50000:
                        await message.channel.send("You don't even have enough money for your degree? Go pick up some garbage.")

                    else:
                        # Deducts money from the user
                        money -= 50000

                        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                        # Gives the user their masters degree by incrementing Education further
                        education_study = int(education_study) + 1
                        education_study = str(education_study) + ".day_wait"

                        db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                        db_conn.commit()

                        # Gives the user a KP point
                        await kp_points()

                        await message.channel.send("Okay, fine, earning a masters is a little impressive. Here you go.")



            # Pre PHD degree
            elif int(education_study) > 70 and int(education_study) < 90:

                await message.channel.send("Study is love. Study is life. Wait, what was the goal of all this again?" +
                                           "\nYou are now " + str(int(education_study) - 70) + "/20th done getting your PHD.")

                education_study = int(education_study) + 1
                education_study = str(education_study) + ".day_wait"

                db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                db_conn.commit()

                # Gives the user a KP point
                await kp_points()



            # Finished PHD degree
            elif int(education_study) == 70:

                # Prompts the user for how much they'll be spending, and asks for them to confirm
                bot_message = await message.channel.send("You've completed your studies for the PHD. However you must pay 100,000$ to get it." +
                                                         "\nPlease type CONFIRM to pay 100,000$ for your PHD. If you do not want to do this then simply do nothing. This will timeout in 30 seconds.")

                # A really weird way to get multiple user replies
                def stock_purchase_check(user_reply):

                    return user_reply.content.lower() == 'confirm' and message.author.id == user_reply.author.id

                try:
                    user_reply = await client.wait_for('message', timeout=30.0, check=stock_purchase_check)

                except asyncio.TimeoutError:

                    await message.channel.send("We don't need no education~")

                else:
                    # Checks if the user even has enough money
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                    money = money.fetchone()
                    money = float(money[0])

                    if money < 100000:
                        await message.channel.send("You don't even have enough money for your degree? Just make an OnlyFans.")

                    else:
                        # Deducts money from the user
                        money -= 100000

                        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                        # Gives the user their PHD by incrementing Education further
                        education_study = int(education_study) + 1
                        education_study = str(education_study) + ".day_wait"

                        db_conn.execute("UPDATE Members SET Education = ? WHERE User_ID = ?", (education_study, message.author.id))
                        db_conn.commit()

                        # Gives the user a KP point
                        await kp_points()

                        await message.channel.send(
                            "Sure you're a world-class professional on the subject you studied, but are you truly happy? Here's your PHD.")
