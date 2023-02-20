

# Initially made back in January 7, 2021. But split into its own file on May 5th, 2021
# May 8th, added the variable time between jobs from Black Market upgrades



async def Jobs(message, db_conn, users_in_job, client, time, random, asyncio):

        # Fetches the time (in universal time) from the database so we know when the user last did -jobs
        last_job_time = db_conn.execute("SELECT Last_Job_Time FROM Members WHERE User_ID = " + str(message.author.id))
        last_job_time = last_job_time.fetchone()

        # Formatting the current time and subtracting last_job_time from it to get how many seconds it's been since they did a job
        replacement_job_time = time.time()
        replacement_job_time = round(replacement_job_time)

        last_job_time = replacement_job_time - last_job_time[0]

        print("It's been", last_job_time, "seconds since they completed a job")



        # This checks the Black Market inventory to see what upgrades the user has

        BM_data = db_conn.execute("SELECT * FROM Black_Market WHERE User_ID = " + str(message.author.id))
        BM_data = BM_data.fetchone()

        # Default 8 hours
        time_check = 28800

        if BM_data[3] == 'Owned':
            time_check = 25200 # 7 hours

        if BM_data[4] == 'Owned':
            time_check = 21600 # 6 hours

        if BM_data[5] == 'Owned':
            time_check = 18000 # 5 hours

        if BM_data[6] == 'Owned':
            time_check = 14400 # 4 hours

        if BM_data[7] == 'Owned':
            time_check = 10800 # 3 hours

        if BM_data[8] == 'Owned':
            time_check = 72000 # 2 hours

        if BM_data[9] == 'Owned':
            time_check = 36000 # 1 hour



        # This checks if it's been enough time (1 to 8 hours) since they last completed a job
        if last_job_time < time_check:

            remainder = time_check - last_job_time

            await message.channel.send("Sorry, you have " + str((time.strftime('%H:%M:%S', time.gmtime(remainder)))) + " time left before you can work a job again. Liberal laws and all that. :sick:")

        else:
            # Checks if the poster is already doing a job or not
            if message.author.id in users_in_job:
                await message.channel.send('You already have a job to do!')

            else:
                # Adds the user to the list of people doing jobs
                users_in_job.append(message.author.id)

                await message.channel.send('You apply for a job...')

                print("Pass one: Selecting random job")

                # This decides what job type will be chosen
                random_job = random.randint(1, 5)

    ###--------------------------------------------------------------------------------------###
                # This goes to the math game (Functional, needs more variants, needs Job 5 structure)
                if random_job == 1:

                    #Defines the necessary function to await the user response
                    def math_check(response):
                        print("Pass math game")

                        # Function only ends if the user answers correctly or leaves the job
                        return (response.content == str(math_answer) or response.content == '-leave job' or response.content == '-leave jobs') and message.author.id == response.author.id and response.channel == message.channel

                    time.sleep(1)
                    await message.channel.send('It\'s time for... math!')
                    time.sleep(1)

                    math_chance = random.randint(1, 2)

                    if math_chance == 1:

                        #This creates the math problem in the form of (a + b) - c^2 + √d

                        math_a = random.randint(3, 30)
                        math_b = random.randint(3, 30)
                        math_c = random.randint(2, 5)
                        math_d = random.randint(3, 20)

                        #Assign the answer before multiplying math_d by itself
                        math_answer = (math_a + math_b) - (math_c * math_c) + math_d

                        print("Math answer is: " + str(math_answer))

                        math_d = math_d * math_d

                        print("(" + str(math_a) + " + " + str(math_b) + ") - " + str(math_c) + "^2 + √" + str(math_d))

                        await message.channel.send(" What is: (" + str(math_a) + " + " + str(math_b) + ") - " + str(math_c) + "^2 + √" + str(math_d) + "?")

                        user_reply = await client.wait_for('message', check=math_check)

                    if math_chance == 2:
                        # This creates the math problem in the form of (c^2 + b) * (a - √d) + e

                        math_a = random.randint(5, 50)
                        math_b = random.randint(5, 50)
                        math_c = random.randint(3, 8)
                        math_d = random.randint(5, 20)
                        math_e = random.randint(3, 25)

                        # Assign the answer before multiplying math_d by itself
                        math_answer = (((math_c * math_c) + math_b) * (math_a - math_d)) + math_e

                        print("Math answer is: " + str(math_answer))

                        math_d = math_d * math_d

                        print("(" + str(math_c) + "^2 + " + str(math_b) + ") * (" + str(math_a) + " - √" + str(math_d) + ") + " + str(math_e))

                        await message.channel.send(" What is: (" + str(math_c) + "^2 + " + str(math_b) + ") * (" + str(math_a) + " - √" + str(math_d) + ") + " + str(math_e) + "?")

                        user_reply = await client.wait_for('message', check=math_check)

                    #Checks if the user gave the correct answer
                    if user_reply.content == str(math_answer):

                        # Generates a original low dollar amount for the job
                        earnings = random.randint(300, 600) / 100

                        answered_correctly = True





    ###--------------------------------------------------------------------------------------###
                # This goes to the ordering game (Functional, but could use different difficulties with different payouts. Needs Job 5 structure)
                if random_job == 2:

                    #Defines the necessary function to await the user response
                    def ordering_check(response):

                        #Function only ends if the user answers correctly or leaves the job
                        return (response.content == string_sorted_number_list or response.content == '-leave job' or response.content == '-leave jobs') and message.author.id == response.author.id and response.channel == message.channel

                    time.sleep(1)
                    await message.channel.send('It\'s time for... ordering!')
                    time.sleep(1)

                    random_number_list = []

                    order_chance = random.randint(1, 2)

                    if order_chance == 1:

                        # Generates a series of 10 random numbers
                        for number in range(0, 10):

                            random_number = random.randint(1, 100)

                            random_number_list.append(random_number)



                    if order_chance == 2:

                        # Generates a series of 12 random numbers
                        for number in range(0, 10):

                            random_number = random.randint(-10, 10)

                            random_number_list.append(random_number)



                    # Converts the list of random numbers into a string of random numbers
                    string_random_number_list = ''

                    for number in random_number_list:
                       string_random_number_list = string_random_number_list + str(number) + " "

                    string_random_number_list = string_random_number_list[:-1]

                    # Converts the list of random numbers into a string of sorted numbers
                    random_number_list.sort()

                    string_sorted_number_list = ''

                    for number in random_number_list:
                       string_sorted_number_list = string_sorted_number_list + str(number) + " "

                    string_sorted_number_list = string_sorted_number_list[:-1]

                    await message.channel.send('Type in order these numbers from least to greatest: ' + string_random_number_list )

                    user_reply = await client.wait_for('message', check=ordering_check)



                    #Checks if the user gave the correct answer
                    if user_reply.content == string_sorted_number_list:

                        # Generates a original low dollar amount for the job
                        earnings = random.randint(500, 800) / 100

                        answered_correctly = True





    ###--------------------------------------------------------------------------------------###
                # This goes to the quiz game (Functional but needs Job 5's structure, and dynamic answering(maybe?))
                if random_job == 3:

                    #Defines the necessary function to await the user response
                    def quiz_check(response):

                        #Function only ends if the user answers correctly or leaves the job
                        return (response.content.lower() == correct_quiz_answer or response.content == '-leave job' or response.content == '-leave jobs') and message.author.id == response.author.id and response.channel == message.channel

                    time.sleep(1)
                    await message.channel.send('It\'s time for... a quiz!')
                    time.sleep(1)

                    # This decides which quiz to post
                    quiz_decider = random.randint(1, 15)

                    if quiz_decider == 1:
                        await message.channel.send("What is the 6th largest country? (Type the answer below.)")
                        correct_quiz_answer = "australia"

                    if quiz_decider == 2:
                        await message.channel.send("The zodiac sign 'Cancer' refers to what animal? (Type the answer below.)")
                        correct_quiz_answer = "crab"

                    if quiz_decider == 3:
                        await message.channel.send("What's the hottest planet in the Solar System? (Type the answer below.)")
                        correct_quiz_answer = "venus"

                    if quiz_decider == 4:
                        await message.channel.send("What is Scotland's national animal? (Type the answer below.)")
                        correct_quiz_answer = "unicorn"

                    if quiz_decider == 5:
                        await message.channel.send("What is the name (two words) of the smallest unit of measurement? (Type the answer below.)")
                        correct_quiz_answer = "planck length"

                    if quiz_decider == 6:
                        await message.channel.send("What’s the brightest star in the sky? (Type the answer below.)")
                        correct_quiz_answer = "sirius"

                    if quiz_decider == 7:
                        await message.channel.send("Who was the first woman to win a Nobel Prize? (Type the answer below.)")
                        correct_quiz_answer = "marie curie"

                    if quiz_decider == 8:
                        await message.channel.send("What is the most abundant metal in the Earth’s crust? (Type the answer below.)")
                        correct_quiz_answer = "aluminum"

                    if quiz_decider == 9:
                        await message.channel.send("What color is a polar bear’s skin? (Type the answer below.)")
                        correct_quiz_answer = "black"

                    if quiz_decider == 10:
                        await message.channel.send("What was the former name of the city Istanbul? (Type the answer below.)")
                        correct_quiz_answer = "constantinople"

                    if quiz_decider == 11:
                        await message.channel.send("How many ribs are in a human body? (type as a numeric)")
                        correct_quiz_answer = "24"

                    if quiz_decider == 12:
                        await message.channel.send("What's the name of the unit that measures a food's spiciness?")
                        correct_quiz_answer = "scoville"

                    if quiz_decider == 13:
                        await message.channel.send("Where is the Sea of Tranquility located?")
                        correct_quiz_answer = "moon"

                    if quiz_decider == 14:
                        await message.channel.send("What colour is a Himalayan Poppy?")
                        correct_quiz_answer = "blue"

                    if quiz_decider == 15:
                        await message.channel.send("What is the world's longest river")
                        correct_quiz_answer = "nile"



                    user_reply = await client.wait_for('message', check=quiz_check)


                    #Checks if the user gave the correct answer
                    if user_reply.content.lower() == correct_quiz_answer:

                        # Generates a original low dollar amount for the job
                        earnings = random.randint(300, 600) / 100

                        answered_correctly = True





    ###--------------------------------------------------------------------------------------###
                # This goes to the word finder game (Functional but needs some structure rework like Job 5 has)
                if random_job == 4:

                    #Defines the necessary function to await the user response
                    def word_finder_check(response):

                        #Function only ends if the user answers correctly or leaves the job
                        return (response.content == correct_answer or response.content == '-leave job' or response.content == '-leave jobs') and message.author.id == response.author.id and response.channel == message.channel

                    time.sleep(1)
                    await message.channel.send('It\'s time for... word finder!')
                    time.sleep(1)

                    #This decides which spelling task to post (start at 0 for the list!)
                    spelling_list = ["walrus", "firetruck", "saturn", "watermelon", "computer", "zayneisgay", "personality", "chocolate", "shopping", "guidance", "ascension", "kirbo", "midnight", "samurai", "telephone"]

                    random_characters_list = ["!", "@", "#", "$", "%", "^", "&", "(", ")", "[", "]", "{", "}", ":", "+", "<", ">", "?", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

                    chosen_string = ""

                    correct_answer = ""

                    for character in spelling_list[random.randint(0, len(spelling_list) - 1)]:

                        for x in range(random.randint(1, 10)):

                            chosen_string += random_characters_list[random.randint(0, len(random_characters_list) - 1)]

                        possible_uppercase = random.randint(0,1)

                        if possible_uppercase == 1:
                            character = character.upper()

                        correct_answer += character

                        chosen_string += character


                    print(chosen_string)
                    print(correct_answer)

                    await message.channel.send("""What word is in the scrambled text? (Type the answer's characters capitalized as they appear)\n""" + chosen_string)


                    user_reply = await client.wait_for('message', check=word_finder_check)

                    #Checks if the user gave the correct answer
                    if user_reply.content == correct_answer:

                        # Generates a original low dollar amount for the job
                        earnings = random.randint(400, 700) / 100

                        answered_correctly = True





    ###--------------------------------------------------------------------------------------###
                # This goes to the reaction game (DONE)
                if random_job == 5:

                    reaction_list = ["👑", "🍑", "🥁", "<:corona:688565883286978643>", "🚀", "🧱", "🏀", "🍿", "🦉", "👺", "🐶", "🧠", "🌮", "🛏️", "🍕"]

                    chosen_reaction = random.choice(reaction_list)

                    # Initial prompt by the bot
                    bot_message = await message.channel.send("Send me that " + chosen_reaction + " reaction, mate.")

                    # A really weird way to get multiple user replies
                    def reaction_check(user_reply, responding_user):

                        # I wasn't sure how to get the name and ID from message.author so I had to shorten responding user to just the name
                        responding_user = str(responding_user)[:-5]

                        # Made this just to support Zayne's 'corona' emoji with normal emojis
                        try:
                            if 'corona' in user_reply.emoji.name:
                                print("Emote is", user_reply.emoji)
                                print("Reaction is", chosen_reaction)
                                user_reply.emoji = chosen_reaction
                        except AttributeError:
                            pass

                        print("Emote is", user_reply.emoji)


                        return user_reply.emoji == chosen_reaction and responding_user == message.author.name and user_reply.message.id == bot_message.id

                    try:
                        #user_reply = the emoji picked and responding_user = mia#1234
                        user_reply, responding_user = await client.wait_for('reaction_add', timeout=15.0, check=reaction_check)

                    except asyncio.TimeoutError:
                        await message.channel.send("'Fraid you took too long, friend.")
                        users_in_job.remove(message.author.id)

                    else:
                        # If the user gets the emoji correct this is triggered
                        if user_reply.emoji == chosen_reaction:

                            # Generates a original low dollar amount for the job
                            earnings = random.randint(300, 700) / 100

                            answered_correctly = True







                # Accrues earnings, posts responses, updates money, updates net worth
                if answered_correctly == True:

                    last_job_time = time.time()

                    last_job_time = round(last_job_time)

                    db_conn.execute("UPDATE Members SET Last_Job_Time = ? WHERE User_ID = ?", (last_job_time, message.author.id))
                    db_conn.commit()

                    # Give user some money for getting the correct answer
                    money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
                    money = money.fetchone()
                    money = money[0]

                    print("pre money is", money)

                    # Generates a original low dollar amount for the job
                    #earnings = random.randint(200, 500) / 100

                    print("Initial earnings", earnings)
                    print("Line 2311, Money is:", money)

                    # Checks the user's inventory for pay upgrades
                    user_inventory = db_conn.execute(f"SELECT * FROM Inventory WHERE User_ID = {message.author.id}")
                    user_inventory = user_inventory.fetchone()

                    print(user_inventory)

                    print("Earnings before inventory checks:", earnings)

                    # Checks for resume
                    if user_inventory[3] == 'Owned':
                        print("User has a resume")
                        earnings *= 1.2

                    # Checks for haircut
                    if user_inventory[4] == 'Owned':
                        print("User has a haircut")
                        earnings *= 1.4

                    # Checks for suit
                    if user_inventory[6] == 'Owned':
                        print("User has a suit")
                        earnings *= 1.6

                    # Checks for car
                    if user_inventory[7] == 'Owned':
                        print("User has a car")
                        earnings *= 1.8

                    # Checks for accountant
                    if user_inventory[8] == 'Owned':
                        print("User has an accountant")
                        earnings *= 2

                    print("Earnings after inventory checks and before education checks:", earnings)

                    # Now checks for education level
                    education_level = db_conn.execute(f"SELECT Education FROM Members WHERE User_ID = {message.author.id}")
                    education_level = education_level.fetchone()
                    education_level = education_level[0]
                    education_level = education_level.split(".")  # Checks if it has the '.day_wait' tag and removes it if it's present
                    education_level = int(education_level[0])

                    # Checks the various education tiers and applies bonuses where needed
                    if education_level > 90:
                        print("User has a PHD")
                        earnings *= 1.2 * 1.4 * 1.6 * 1.8 * 2

                    elif education_level > 70:
                        print("User has a Masters")
                        earnings *= 1.2 * 1.4 * 1.6 * 1.8

                    elif education_level > 50:
                        print("User has a Bachelors")
                        earnings *= 1.2 * 1.4 * 1.6

                    elif education_level > 30:
                        print("User has an Associates")
                        earnings *= 1.2 * 1.4

                    elif education_level > 10:
                        print("User has an Associates")
                        earnings *= 1.2

                    else:
                        print("User has no education")

                    print("Earnings after education checks:", earnings)


                    # Checks the user's KP inventory for pay upgrades
                    kp_inventory = db_conn.execute(f"SELECT * FROM KP_Inventory WHERE User_ID = {message.author.id}")
                    kp_inventory = kp_inventory.fetchone()

                    print(kp_inventory)

                    print("Earnings before KP inventory checks:", earnings)

                    # Checks for Kill la Kill Poster
                    if kp_inventory[3] == 'Owned':
                        print("User has a KLK Poster")
                        earnings *= 1.04

                    # Checks for Naruto Headband
                    if kp_inventory[4] == 'Owned':
                        print("User has a Naruto Headband")
                        earnings *= 1.09

                    # Checks for Pikachu Shirt
                    if kp_inventory[5] == 'Owned':
                        print("User has a Pikachu Shirt")
                        earnings *= 1.14

                    # Checks for Kirby Plushie
                    if kp_inventory[6] == 'Owned':
                        print("User has a Kirby Plushie")
                        earnings *= 1.19

                    # Checks for Waifu Pillow
                    if kp_inventory[7] == 'Owned':
                        print("User has a Waifu Pillow")
                        earnings *= 1.24

                    # Checks for Husbando Pillow
                    if kp_inventory[8] == 'Owned':
                        print("User has a Husbando Pillow")
                        earnings *= 1.29

                    # Checks for All might Action figure
                    if kp_inventory[9] == 'Owned':
                        print("User has an All might Action figure")
                        earnings *= 1.34

                    # Checks for Eva Statue
                    if kp_inventory[10] == 'Owned':
                        print("User has an Eva Statue")
                        earnings *= 1.39

                    # Checks for Gurren Lagann Mecha Toy
                    if kp_inventory[11] == 'Owned':
                        print("User has a Gurren Lagann Mecha Toy")
                        earnings *= 1.44

                    # Checks for God Tongue
                    if kp_inventory[12] == 'Owned':
                        print("User has THE GOD TONGUE")
                        earnings *= 1.49

                    print("Earnings after KP inventory checks:", earnings)


                    # Applies earnings to money
                    earnings = round(earnings, 2)
                    money += earnings


                    # Posts the job related response to the channel
                    if random_job == 1:
                        await message.channel.send('You either mathed or googled that correctly. You earned ' + str(earnings) + "$ from this job.")

                    if random_job == 2:
                        await message.channel.send('You ordered the numbers correctly. You earned ' + str(earnings) + "$ from this job.")

                    if random_job == 3:
                        await message.channel.send('You answered correctly. You earned ' + str(earnings) + "$ from this job.")

                    if random_job == 4:
                        await message.channel.send('You got the right word. You earned ' + str(earnings) + "$ from this job.")

                    if random_job == 5:
                        await message.channel.send('Looks like you correctly reacted in time. You earned ' + str(earnings) + "$ from this job.")



                    # Adds a KP point to the user
                    REMOVED FOR GITHUB_point = db_conn.execute(f"SELECT KP FROM Members WHERE User_ID = {message.author.id}")
                    REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point.fetchone()
                    REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point[0]

                    REMOVED FOR GITHUB_point += 1

                    db_conn.execute(f"UPDATE Members SET KP = {REMOVED FOR GITHUB_point} WHERE User_ID = {message.author.id}")
                    db_conn.commit()



                    # Updates the user's money
                    db_conn.execute(f"UPDATE Members SET Money = {money} WHERE User_ID = {message.author.id}")
                    db_conn.commit()

                    print('Pass user removed from jobs')
                    users_in_job.remove(message.author.id)

                    print("Job fully done and user paid!")


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

                    print("User's net worth updated. FULLY DONE")