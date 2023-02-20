# Written December 6th, 2020. Ported code from Leia's incomplete point system.
# December 27, 2020 - Updated to include 'intents' to access server member lists and data. Added the ability to check other member's money.
# December 28, 2020 - Added threading for asynchronous functionality
# December 29, 2020 - Added -top and began initial work on stocks
# January 7, 2021 - Began implementing -jobs and also the first use of asynchronous user responses to a bot
# January 17, 2021 - Finished adding -lottery feature. Worked on -jobs more. Nearly finished.
# January 24, 2021 - Began work on saving user finances, plotting, and uploading image plots. Need to wait for financial data to collect first
# January 28, 2021 Began work on -shop, -education, -bank, finished up -stocks
# February 2, 2021 Began work on -rob feature. I hate it.
# May 2, 2021 - Began work splitting the code base into multiple files for easier development and maintenance.
# June 17, 2021, been fixing various small bugs, improved certain things like -piechart and -jobs and -timeline



# Personal sub-files related to the project
from Black_Market import *
from Shop import *
from Jackpot import *
from Stocks import *
from Jobs import *
from Education import *
from KP_Shop import *
from Bank import *
from Rob import *
from Lottery import *
from Timeline import *
from Asyncio_Scheduler import *
from Top_Profile_Pay import *
from Piechart import *



import discord

# Allows the bot to get member server member lists and certain data
intents = discord.Intents.default()
intents.members = True

from discord.ext import commands, tasks

import asyncio
import random
import sqlite3
import sys
import time
import datetime
import schedule
import threading
#import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# For doge coin website requests and importing data
import urllib.request
from bs4 import BeautifulSoup

import logging
logging.basicConfig(level=logging.INFO)




# Must be set like this to get member name via their IDs
client = discord.Client(intents=intents)
#client = discord.Client()






# 9pm - Jackpot clears out

# 11:30 (Sunday) - Pays weekly dividends to stock holders

# 11:57 - Companies history
# 11:59 - Member history

# 12:01 - Education detagger
# 12:03 - Bank interest
# 12:05 - Stocks adjustment

# 4am - Lottery resets





# Creates a separate thread where lottery tickets are reset
# https://pypi.org/project/schedule/
def thread_test():
    print("Thread start")

    def job():
        print("Threading working")
        #Accrues interests and taxes logic here


    def lottery_reset():
        db_conn = sqlite3.connect('economy_game.db')

        db_conn.execute("Update Members SET Lottery_Count = 0")
        db_conn.commit()

        print("Successfully reset everyone to 0 lottery tickets at 4am.")



    schedule.every().day.at("14:39").do(job)

    schedule.every().day.at("04:00").do(lottery_reset)


    while True:
        #print("While true loop working")
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=thread_test, args=())
thread.start()






# Updates the post in REMOVED FOR GITHUB's server to reflect the richest members once a minute
post_updater_task = asyncio.ensure_future(richest_post_updater(sqlite3, asyncio, client))





# Updates the post in REMOVED FOR GITHUB's server to reflect general company and stock information once a minute
stocks_updater_task = asyncio.ensure_future(stocks_post_updater(sqlite3, asyncio, client))





# Updates the net worth of users every minute, set off by 30 seconds, in the database 30 seconds into every minute

# net_worth_database_updater_task = asyncio.ensure_future(net_worth_database_updater(sqlite3, datetime, asyncio))

# TURN THIS ON IF NET WORTHS AREN'T FULLY UPDATING WITH THINGS SOME TIMES










# Once a week on Sunday at 11:30pm people with stocks are paid dividen payments of profit over the last week
weekly_dividend_payout_task = asyncio.ensure_future(stock_dividend_payout(datetime, sqlite3, client, asyncio))









# Jackpot function to pay out once a day the winner (if there is one) at 9pm
daily_jackpot_task = asyncio.ensure_future(jackpot_payout(datetime, sqlite3, random, client, asyncio))





# Function to log company stocks once a day at 11:57pm
stocks_history_task = asyncio.ensure_future(stocks_history_logging(datetime, sqlite3, time, asyncio))





# Function to log people's money once per day at 11:59pm
daily_members_history_task = asyncio.ensure_future(members_history_logging(datetime, sqlite3, time, asyncio))





# Removes the 'once a day' tag for people studying at AND company influence tag 12:01am
education_detagger_task = asyncio.ensure_future(education_detagger(datetime, sqlite3, asyncio))





# Money in the bank accrues some interest at 12:03am
bank_interest_accruer_task = asyncio.ensure_future(bank_interest_accruer(datetime, sqlite3, asyncio))





# Once a day the stock market is updated to reflect its trends and alter the company values at 12:05am
stocks_market_updater_task = asyncio.ensure_future(stock_market_updater(datetime, asyncio, sqlite3, random))





# Have a random event happen to a member, sometimes, twice a day at 8am and 8pm
random_member_event_task = asyncio.ensure_future(random_member_event(datetime, sqlite3, random, client, asyncio))















# Bank accurement test
async def bank_test():

    money = 11396
    days = 0

    # Loops once a second to check the time
    while days < 365:


        if money >= 1000 and money < 10000:
            print("Between 1,000 and 10,000")
            money = money * 1.01

        if money >= 10000 and money < 100000:
            print("Between 10,000 and 100,000")
            money = money * 1.02

        if money >= 100000 and money < 1000000:
            print("Between 100,000 and 1,000,000")
            money = money * 1.03

        if money >= 1000000 and money < 10000000:
            print("Between 1,000,000 and 10,000,000")
            money = money * 1.04

        if money >= 10000000 and money < 100000000:
            print("Between 10,000,000 and 100,000,000")
            money = money * 1.05

        if money >= 100000000 and money < 1000000000:
            print("Between 100,000,000 and 1,000,000,000")
            money = money * 1.06

        if money >= 1000000000 and money < 10000000000:
            print("Between 1,000,000,000 and 10,000,000,000")
            money = money * 1.07

        if money >= 10000000000 and money < 100000000000:
            print("Between 10,000,000,000 and 100,000,000,000")
            money = money * 1.08

        if money >= 100000000000 and money < 1000000000000:
            print("Between 100,000,000,000 and 1,000,000,000,000")
            money = money * 1.09

        if money >= 1000000000000 and money < 10000000000000:
            print("Move than 1,000,000,000,000!!!")
            money = money * 1.10





        days += 1

        print("Day", days)

        money = float("%.2f" % round(money, 2))

        money += 100

        print("Money", money)
        print(" ")




        #await asyncio.sleep(0.01)


# bank_test_task = asyncio.ensure_future(bank_test())















# Shows off dogecoin's price and percentage rice/fall in the bot's status
async def dogecoin_price():

    # Loops once a second to check the time
    while True:

        # Gets the HTML from coindesk
        url = 'https://www.coindesk.com/price/dogecoin'
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")

        # A not-the-best-way to get the dogecoin value
        doge_price = soup.findAll("div", class_="price-large")

        print(doge_price)

        doge_price = str(doge_price[0])
        doge_price = doge_price[54:]
        doge_price = doge_price[:4]

        # A not-the-best-way to get the dogecoin percentage rise/fall
        percentage = soup.findAll("span", class_="percent-value-text")

        percentage = str(percentage[0])
        percentage = percentage[33:]
        percentage = percentage[:-7]

        # Compiles the status message (DC meaning Doge Coin)
        status = "DC: " + doge_price + "$ (" + percentage + "%)"

        # Pushes the status to the bot
        activity = discord.Activity(name=status, type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)

        # Does it again every 5 minutes
        await asyncio.sleep(300)


# Muted here as we turn it on below in the first @client_event function
#dogecoin_price_task = asyncio.ensure_future(dogecoin_price())




















# People currently doing a job or not. Must be declared before main logic to be available at all times. Unless made global?
users_in_job = []

# People currently trying to buy stock. Prevents -stocks buy spam and derping the bot. Unless made global?
users_buying_stock = []

# Prompts the console with start and login confirmation
@client.event
async def on_ready():
    print('Logged in as',client.user.name+'!')
    print('Client ID:',client.user.id)
    print('------')

    # Passes the doge coin price updater above into the @client_Event function
    asyncio.ensure_future(dogecoin_price())

    # Muted out so the doge coin prices will work above
    #activity = discord.Activity(name="Making $$$", type=discord.ActivityType.playing)
    #await client.change_presence(activity=activity)

    # Older activity method that doesn't work as well
    #await client.change_presence(activity=discord.Activity(name="Test"))



# This is for message logging just below and isn't super important
message_total = 0

# Establishes the base ki points for the function to use
ki_points = 0

# All the actual logic (duh)
@client.event
async def on_message(message):

    # Lowers the post to lowercase so caps don't keep people from doing commands
    message.content = message.content.lower()


    # Establishes the connection to the database and sets the cursor
    db_conn = sqlite3.connect('economy_game.db')
    theCursor = db_conn.cursor()



    # My 'use a post as storage' idea
    global ki_points

    channel = client.get_channel(REMOVED FOR GITHUB)
    message_to_edit = await channel.fetch_message(REMOVED FOR GITHUB)

    ki_points = int(message_to_edit.content) + len(message.content)

    await message_to_edit.edit(content=str(ki_points))






    # This is purely for private message logging to see what things the bois try to do in the bot's DMs
    if message.guild == None and message.author.id != REMOVED FOR GITHUB: # Doesn't log its own messages
        global message_total

        # Posts to my private channel to log the bois DMs to the bot
        channel = client.get_channel(REMOVED FOR GITHUB)
        await channel.send(str(message.author.name) + " DM'd: \n" + str(message.content))







    # Makes the bot post to a specific channel
    if message.content == '-post' and message.author.id == REMOVED FOR GITHUB:
        channel = client.get_channel(REMOVED FOR GITHUB)
        await channel.send('[Reserved]')






    # For general testing
    if message.content == '-blargh' and message.author.id == REMOVED FOR GITHUB:

        print("nothing")











    # This is purely for debugging and deleting bot messages where needed
    if message.content == "-delete":
        #channel = client.get_channel(REMOVED FOR GITHUB)

        test = await message.channel.fetch_message(REMOVED FOR GITHUB) #Put message ID here

        print(test)

        await test.delete()












    # Send a specific person a message
    if message.content == '-dm message':
        user = client.get_user(REMOVED FOR GITHUB)
        await user.send("Suddenly, REMOVED FOR GITHUB appears and manages to take you by surprise, and they steal 13.41$ from you. Can't trust anyone.")



    # Get the messages in a channel
    if message.content == '-message_history':


        channel = client.get_channel(REMOVED FOR GITHUB)

        messages = await channel.history(limit=100).flatten()

        for message in messages:
            print(message.content)

        print(messages)




    # Plot testing
    if message.content == '-plot':
        plt.plot([32, 150, 14, 29])
        plt.ylabel('Money')
        plt.xlabel("User Name")
        plt.savefig('plot.png')
        plt.show()

        channel = client.get_channel(REMOVED FOR GITHUB)
        await channel.send(file=discord.File('plot.png'))


    # Plot testing with dates
    if message.content == '-plot dates':
        dates = ["01/02/2020", "01/03/2020", "01/04/2020", "01/05/2020", "01/06/2020", "01/07/2020", "01/08/2020"]

        x_values = [datetime.datetime.strptime(d, "%m/%d/%Y").date() for d in dates]
        y_values = [1, 5, 3, 4, 6, 2, 7]

        ax = plt.gca()

        formatter = mdates.DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(formatter)

        locator = mdates.DayLocator()
        ax.xaxis.set_major_locator(locator)

        plt.figure(figsize=(10, 6))

        plt.plot(x_values, y_values)

        plt.savefig('plot.png')

        plt.show()















    # Creating the database and table
    if message.content.startswith('-economy database create') and message.author.id == REMOVED FOR GITHUB:
        def printDB():

            try:
                table = theCursor.execute("SELECT User_ID, Username, Money FROM Members")

                for row in table:
                    print('User ID :', row[0])
                    print('Username :', row[1])
                    print('Money :', row[2])

            except sqlite3.OperationalError:
                print("The Table Doesn't Exist")

            except:
                print("Couldn't Retrieve Data From Database")

        db_conn = sqlite3.connect('economy_game.db')
        print("Database Created")

        theCursor = db_conn.cursor()

        try:
            db_conn.execute("CREATE TABLE Members(User_ID INTEGER NOT NULL, Username TEXT NOT NULL, Money REAL NOT NULL);")

            db_conn.commit()

            print("Table Created")

        except sqlite3.OperationalError:
            print("Table Couldn't Be Created")

        #db_conn.execute("INSERT INTO Members (User_ID, Username, Points, Last_Post) VALUES ('50', 'Mia', 500, date('now'))")

        db_conn.commit()

        printDB()

        db_conn.close()
        print("Database Closed")




    # Displays a helpful message of commands for admins
    if message.content == '-help' and message.author.id == REMOVED FOR GITHUB:
        await message.channel.send('''```   You may use:
        -join      (joins the money makers)
        -money     (checks how much money you have)
        -profile   (check another person's account information -- example: '-profile @user')
        -top       (shows a leaderboard of the richest members in order)
        -pay       (pay someone else money -- example: `-pay @user 10`)
        -jobs      (let's you earn extra monies on the side)
        -leave job (cancels your current job and task)
        -education (earn your diploma and degrees to earn more money)
        -bank      (give or take money from your bank account, keeps it safe and accrues interest)
        -shop      (buy items that can help you)
        -lottery   (you pay for the chance to earn more money, only 4 a day)
        -jackpot   (you and others pay in and one person wins the money at the end of the day)
        -stocks    (buy and sell stocks in the attempt to earn profit)
        -rob       (let's you still money from others, you can DM the bot to do this)
        -timeline  (let's you check user and company stock value over time)
        -piechart  (see the server or specific person's monetary values as a piechart)
        -kp        (shows the REMOVED FOR GITHUB Points store and how much you have)
        -bm        (shows the Black Market information)
        -leave     (not working)
        -trade     (not working)
        -donate    (not working)
        -upgrade   (not working)```''')

    # Displays a helpful message of commands for normal users
    if message.content == '-help' and message.author.id != REMOVED FOR GITHUB:
        await message.channel.send('''```   You may use:
        -join      (joins the money makers)
        -money     (checks how much money you have)
        -profile   (check another person's account information -- example: '-profile @user')
        -top       (shows a leaderboard of the richest members in order)
        -pay       (pay someone else money -- example: `-pay @user 10`)
        -jobs      (let's you earn extra monies on the side)
        -leave job (cancels your current job and task)
        -education (earn your diploma and degrees to earn more money)
        -bank      (give or take money from your bank account, keeps it safe and accrues interest)
        -shop      (buy items that can help you)
        -lottery   (you pay for the chance to earn more money, only 4 a day)
        -jackpot   (you and others pay in and one person wins the money at the end of the day)
        -stocks    (buy and sell stocks in the attempt to earn profit)
        -rob       (let's you still money from others, you can DM the bot to do this)
        -timeline  (let's you check user and company stock value over time)
        -piechart  (see the server or specific person's monetary values as a piechart)
        -kp        (shows the REMOVED FOR GITHUB Points store and how much you have)
        -bm        (shows the Black Market information)
        -leave     (not working)
        -trade     (not working)
        -donate    (not working)
        -upgrade   (not working)```''')







    list_of_supported_Channels = [REMOVED FOR GITHUB, REMOVED FOR GITHUB] # Main and Robo chats only

    # This increments databased members by some amount of money whenever they post. Make sure this is at the top, but AFTER -help commands
    if message.channel.id in list_of_supported_Channels: # Only gives money in REMOVED FOR GITHUB's main server channels

        money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
        money = money.fetchone()

        # Only activates if the user is in the database
        if money != None:

            # On every post they make, the poster's display name is updated in the database
            db_conn.execute("UPDATE Members SET Username = ? WHERE User_ID = ?", (message.author.display_name, message.author.id))
            db_conn.commit()

            # Checks the word length of a post to determine income
            message_split = message.content.split()

            print("Word count:", len(message_split))
            print("Character count:", len(message.content))

            income_influencer = random.randint(60, 160) / 100 # Got a small buff on Feb 15th, 2021. Was originally (50, 150) / 100

            print("Income influence: " + str(income_influencer) + "%")

            average_word_length = 4.7

            # Formula is: ((words / 4.7) + (characters / 4.7)) / 2 then multiplied by the random influencer
            earnings = ((len(message_split) / average_word_length) + (len(message.content) / average_word_length)) / 2
            print("Initial earnings:", earnings)
            earnings = earnings * ((income_influencer / 100))
            print("Initial earnings times influence and after 100 division:", earnings)

            print("Earnings added (after initial random income influence):", earnings)
            print("Earnings added (rounded):", round(earnings, 2))
            print()

            # Makes sure the user gets paid at least a penny
            if earnings < 0.01:
                earnings = 0.01


            # Gets the user's money to add their earnings
            money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
            money = money.fetchone()
            money = money[0]

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
            education_level = education_level.split(".") # Checks if it has the '.day_wait' tag and removes it if it's present
            education_level = int(education_level[0])

            # Checks the various education tiers and applies bonuses where needed
            print("Education level is", education_level)
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
                print("User has a Diploma")
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
            money += earnings
            money = round(money, 2)

            # Updates the user's money
            db_conn.execute(f"UPDATE Members SET Money = {money} WHERE User_ID = {message.author.id}")
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










    # Adds user to database
    if message.content.startswith('-join'):

        #Attempts to fetch the joinining member's ID from the database (if it's there)
        check_if_present = db_conn.execute("SELECT User_ID FROM Members WHERE User_ID = " + str(message.author.id))
        check_if_present = check_if_present.fetchone()

        #Conditional statement if the member is in the database or not already
        if check_if_present != None:

            await message.channel.send('You\'re already a cog in the capitalistic machine! :money_mouth:')

        elif check_if_present == None:
            db_conn.execute("INSERT INTO Members (User_ID, Username, Nickname, Net_Worth, Money, Bank, Stock_Value, Last_Job_Time, Lottery_Count, Jackpot_Amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.author.id, message.author.display_name, "[Placeholder]", 0, 0, 0, 0, 0, 0, 0))
            db_conn.commit()

            await message.channel.send('Welcome to the destruction of all moral values! :moneybag:')









    # User removes themself from their team
    if message.content == '-leaveeeeeerererere': #Broken for now

        check_if_present = db_conn.execute("SELECT Team FROM Members WHERE User_ID = " + str(message.author.id))
        check_if_present = check_if_present.fetchone()

        #Checks first if the user is in the database
        if check_if_present == None or check_if_present[0] == 'No Team':

            await message.channel.send('You already don\'t have a chosen team. :no_entry_sign:')

        else:
            team = 'No Team'

            db_conn.execute("UPDATE Members SET Team = ? WHERE User_ID = ?", (team, message.author.id))
            db_conn.commit()

            await message.channel.send('You have abandoned your team. :white_check_mark:')








    # Calls to post the richest members in order of highest money
    if message.content.startswith("-top"):

        await Top(db_conn, message)












    # Gets the user's money # Obsolete, ignore it!
    if message.content == '-moneyyyyyyyyyyyyyyyyyyyyy': #Obsolete feature

        money = db_conn.execute("SELECT Money FROM Members WHERE User_ID = " + str(message.author.id))
        money = money.fetchone()

        #This ensures a trailing zero (like 100.70$ instead of 100.7$)
        output_money = "%.2f" % round(money[0], 2)

        await message.channel.send('Money : ' + output_money + '$')
















    # Basically triggers getting only the user's economic profile information
    if message.content.startswith("-profile") or message.content.startswith("-money") or message.content.startswith("-balance"):

        await Profile(message, db_conn, discord)













    # Lets a user pay / give money to another user
    if message.content.startswith('-pay'):

        await Pay(message, time, db_conn)













    # Adding various jobs users can do to earn monies (also utilizes my first use of users responding multiple times asynchronously)
    if message.content == '-jobs' or message.content == '-job' and message.guild != None:

        await Jobs(message, db_conn, users_in_job, client, time, random, asyncio)






    # User leaves their current job (a general fail-safe in case the -jobs logic messes up or the job message is deleted)
    if message.content == '-leave job' or message.content == '-leave jobs' or message.content == '-job leave' or message.content == '-jobs leave':
        #Checks, then removes the user's ID from the job list if it's present
        if message.author.id in users_in_job:
            users_in_job.remove(message.author.id)
            await message.channel.send('You left your job. Got sick of sales?')
        else:
            await message.channel.send('You don\'t even have a job, you lazy bum!')















    # Prompts for the education sub-functions
    if message.content == '-education' or message.content == "-education help":

        await EducationPrompt(message)


    if message.content.startswith("-education") and (message.content != '-education' or message.content != "-education help") and message.guild != None:

        await Education(message, db_conn, client, asyncio)















    # Prompts for the bank sub-functions
    if message.content == '-bank' or message.content == "-bank help":

        await BankPrompt(message)



    if (message.content.startswith("-deposit") or message.content.startswith("-withdraw") or message.content.startswith("-bank")) and (message.content != '-bank' or message.content != "-bank help") and (message.guild != None):
        print(message.guild)
        await Bank(message, db_conn)


















    # Prompts for the shop sub-functions
    if message.content == '-shop' or message.content == "-shop help" or message.content == "-shop info":

        await ShopPrompt(message)

    # Actually lets people buy from the shop
    if message.content.startswith("-shop buy") and (message.content != '-shop' or message.content != "-shop help" or message.content == "-shop info")  and message.guild != None:

        await Shop(message, db_conn)



















    # Prompts for the KP shop sub-functions
    if message.content == '-kp' or message.content == "-kp help" or message.content == "-kp info":

        await KP_Prompt(message, db_conn)



    # Spends KP to buy a voucher / lottery ticket
    if message.content == '-kp voucher':

        await KP_Voucher(message, db_conn, time, random)



    # Actually lets people buy from the shop
    if message.content.startswith("-kp buy") and (message.content != '-kp' or message.content != "-kp help" or message.content == "-kp info") and message.guild != None:

        await KP_Shop(message, db_conn)




















    # Tests the black market store (and pushing functions outside of the main thread)
    if message.content == '-bm' or message.content == '-bm help' or message.content == '-bm info' or message.content == '-black market' or message.content == "-black market help" or message.content == "-black market info":
        await BlackMarketPrompt(message)

    if message.content.startswith("-bm buy") and (message.content != '-bm' or message.content != '-black market' or message.content != "-black market help" or message.content == "-black market info") and message.guild != None:
        await BlackMarket(message, db_conn)



















    # Purely for testing lottery payout rates CAN BE DELETED
    if message.content == '-lottery test':
        lottery_100_winnings = [*(0 * [0]), *(2 * [1]), *(4 * [2]), *(6 * [5]), *(8 * [10]), *(9 * [20]), *(10 * [25]), *(16 * [50]), *(29 * [100]), *(9 * [250]), *(6 * [500]), *(1 * [1000])]

        print(sum(lottery_100_winnings))
        print(len(lottery_100_winnings))

        print("Average payout is:", sum(lottery_100_winnings) / len(lottery_100_winnings))



    # Informs the user how the -lottery command and tickets work
    if message.content == '-lottery' or message.content == '-lottery help':

        await LotteryPrompt(message)



    # Actually purchases a lottery ticket for the user
    if message.content == '-lottery 1' or message.content == '-lottery 5' or message.content == '-lottery 10' or message.content == '-lottery 25' or message.content == '-lottery 50' or message.content == '-lottery 100' and message.guild != None:

        await Lottery(message, db_conn, time, random)
















    # Prompts jackpot information
    if message.content == "-jackpot":

        await JackpotPrompt(message, db_conn)


    # Actually uses the jackpot
    if message.content.startswith("-jackpot") and message.content != "-jackpot" and message.guild != None:

        await Jackpot(message, db_conn)















    # Prompts basic stocks information
    if message.content == '-stocks' or message.content == '-stocks help':
        await StocksPrompt(message)


    # Checks your stocks
    if message.content.startswith('-stocks') and message.content != '-stocks' and message.guild != None:
        await Stocks(message, db_conn, users_buying_stock, client, asyncio, random)


















    # Returns the -rob informaiton post
    if message.content == '-rob' or message.content == '-rob help':

        await RobPrompt(message)


    # You freaking rob people here
    if message.content.startswith('-rob') and message.content != '-rob':

        await Rob(message, db_conn, time, random, client)

















    # Posts helpful commands for the user so they can use the -timeline feature
    if message.content == '-timeline' or message.content == '-timeline help':
        await TimelinePrompt(message)

    # Attempt for actual implementation of graphs with dates and user called data
    if message.content.startswith('-timeline') and message.content != '-timeline' and message.content != '-timeline help':
        await Timeline(message, db_conn, plt, discord)















    # Displays helpful message for piechart command
    if message.content == '-piechart' or message.content == '-piechart help' or message.content == '-piechart info':
        await PiechartPrompt(message)

    # Calls a server or specific member piechart related to various monetary values
    if message.content.startswith('-piechart'):
        await Piechart(message, db_conn, plt, discord)
















# Turns off SCRIPT
    if message.content == '-sleep' and message.author.id == REMOVED FOR GITHUB:
        await client.logout()




client.run(REMOVED FOR GITHUB)