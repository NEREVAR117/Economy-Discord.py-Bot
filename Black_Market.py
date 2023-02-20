
# Began making this on May 5th, 2021, completed on May 8th, 2021



async def BlackMarketPrompt(message):
    # Prompts for the shop sub-functions
    await message.channel.send("""You can purchase the following items:
```    [1] Hire the homeless to work for you - 200$ and 60KP (Do a job every 7 hours)
    [2] Hire teenagers for cheap labor - 800$ and 80KP (Do a job every 6 hours)
    [3] Hire desperate people for side hussles - 3,000$ and 120KP (Do a job every 5 hours)
    [4] Hire foreign workers for dollars an hour - 8,000 and 140KP (Do a job every 4 hours)
    [5] Hire thugs to steal and loot for you - 12,000$ and 160kp (Do a job every 3 hours)
    [6] Hire children for pennies an hour in poor nations - 20,000$ and 200KP (Do a job every 2 hours)
    [7] Buy literal child slaves to work the mines for you - 40,000 and 250KP (Do a job every hour)
    
    [8] A crooked accountant to cook your books - 10,000 and 150KP (Do jobs automatically every 8 hours at 25% income)
    [9] Buy mercenaries to handle your money and black markets - 40,000 and 250KP (Do jobs automatically every 6 hours at 50% income)
    [10] Bribe politicians to look the other way on your activities - 100,000 and 400KP (Do jobs automatically every 4 hours at 75% income)
    [11] Fund warlords against weak democracies to secure national loot - 250,000 and 700KP (Do jobs every 2 hours at 100% income)```

```    [12] Proxy purchasing, buy 2 lottery tickets a day - 100$ and 20KP
    [13] Proxy purchasing, buy 3 lottery tickets a day - 250$ and 40KP
    [14] Proxy purchasing, buy 4 lottery tickets a day - 500$ and 80KP
    [15] Proxy purchasing, buy 5 lottery tickets a day - 1,000$ and 100KP
    [16] Proxy purchasing, buy 6 lottery tickets a day - 2,500$ and 120KP
    [17] Proxy purchasing, buy 7 lottery tickets a day - 5,000$ and 160KP
    [18] Proxy purchasing, buy 8 lottery tickets a day - 10,000$ and 200KP
    
    [19] Bribe the teller, get slightly better odds of winning - 2,500 and 100KP
    [20] Bribe the lottery administration, get two tickets and choose the larger payout - 25,000 and 300KP```

    Type `-bm buy X` where X is the item's number to purchase it.""")




async def BlackMarket(message, db_conn):
    # Actually lets people buy from the shop
    print("Black market shop works")

    split_message = message.content.split()

    # The message to print to the user
    shop_items = {'1': 'Missing teeth and all, you\'ve hired the needy off the streets.',
                  '2': 'Teenagers are stupid and want cash for drugs. This is easy money.',
                  '3': 'Former criminals, drug addicts, these people are desperate for side work.',
                  '4': 'Cheap labor comes from abroad. Tap into it for capital interests.',
                  '5': 'Thievery is natural part of capitalism when you really think about it.',
                  '6': 'Children are an excellent method of maximizing profits.',
                  '7': 'The world is cruel. You may as well be the one with the whip.',
                  '8': 'Gang and mob connections have its benefits.',
                  '9': 'Mercenaries enjoy the perks of ignoring certain laws.',
                  '10': 'The natural result of capitalism and democracy is for capitalists to own democracy.',
                  '11': 'In this case, might truly makes right. Who is left to tell you otherwise?',

                  '12': 'Through a proxy purchaser, you can now buy 2 lottery tickets a day.',
                  '13': 'Through a proxy purchaser, you can now buy 3 lottery tickets a day.',
                  '14': 'Through a proxy purchaser, you can now buy 4 lottery tickets a day.',
                  '15': 'Through a proxy purchaser, you can now buy 5 lottery tickets a day.',
                  '16': 'Through a proxy purchaser, you can now buy 6 lottery tickets a day.',
                  '17': 'Through a proxy purchaser, you can now buy 7 lottery tickets a day.',
                  '18': 'Through a proxy purchaser, you can now buy 8 lottery tickets a day.',
                  '19': 'The teller is now working for you, and will give tickets with higher payout rates.',
                  '20': 'Well, that\'s just cheating.'}


    # The column name the SQL database needs
    sql_names = {'1': 'Homeless',
                 '2': 'Teenagers',
                 '3': 'Desperate',
                 '4': 'Foreigners',
                 '5': 'Looters',
                 '6': 'Children',
                 '7': 'Slaves',
                 '8': 'Accountant',
                 '9': 'Mercenaries',
                 '10': 'Politicians',
                 '11': 'Warlords',

                 '12': 'Proxy_1',
                 '13': 'Proxy_2',
                 '14': 'Proxy_3',
                 '15': 'Proxy_4',
                 '16': 'Proxy_5',
                 '17': 'Proxy_6',
                 '18': 'Proxy_7',
                 '19': 'Teller',
                 '20': 'Lottery'}


    # The monetary cost of the upgrade
    items_money_cost = {'1': 200,
                        '2': 800,
                        '3': 3000,
                        '4': 8000,
                        '5': 12000,
                        '6': 20000,
                        '7': 40000,
                        '8': 10000,
                        '9': 40000,
                        '10': 100000,
                        '11': 250000,
                        '12': 100,
                        '13': 250,
                        '14': 500,
                        '15': 1000,
                        '16': 2500,
                        '17': 5000,
                        '18': 10000,
                        '19': 2500,
                        '20': 25000}

    # The KP cost of the upgrade
    items_kp_cost = {'1': 60,
                     '2': 80,
                     '3': 120,
                     '4': 140,
                     '5': 160,
                     '6': 200,
                     '7': 250,
                     '8': 150,
                     '9': 250,
                     '10': 400,
                     '11': 700,
                     '12': 20,
                     '13': 40,
                     '14': 80,
                     '15': 100,
                     '16': 120,
                     '17': 160,
                     '18': 200,
                     '19': 100,
                     '20': 300}



    # Check if they already own the item they're trying to buy
    print(shop_items[split_message[2]])

    item_check = db_conn.execute('SELECT (%s) FROM Black_Market WHERE User_ID = ?' % (sql_names[split_message[2]]), (message.author.id,))
    print(item_check)
    item_check = item_check.fetchone()
    print(item_check)
    item_check = item_check[0]
    print(item_check)

    if item_check == 'Owned':
        await message.channel.send("You've already purchased that.")

    else:
        # Checks if they even have enough money
        money = db_conn.execute('SELECT Money FROM Members WHERE User_ID = ?', (message.author.id,))
        money = money.fetchone()
        money = money[0]

        if money < items_money_cost[split_message[2]]:
            await message.channel.send("Bro. You're gonna need more cash for this operation.")

        else:
            # Checks if they even have enough KP points
            KP = db_conn.execute('SELECT KP FROM Members WHERE User_ID = ?', (message.author.id,))
            KP = KP.fetchone()
            KP = KP[0]

            if KP < items_kp_cost[split_message[2]]:
                await message.channel.send("You're gonna have to earn more KP for this. Come back later.")

            else:

                # Gives the user the upgrade
                db_conn.execute("UPDATE Black_Market SET (%s) = ? WHERE User_ID = ?" % (sql_names[split_message[2]]), ("Owned", message.author.id))

                money -= items_money_cost[split_message[2]]
                KP -= items_kp_cost[split_message[2]]

                money = "%.2f" % round(money, 2)

                db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))

                db_conn.execute("UPDATE Members SET KP = ? WHERE User_ID = ?", (KP, message.author.id))

                db_conn.commit()


                await message.channel.send(shop_items[split_message[2]])


                # Adds a KP point to the user
                REMOVED FOR GITHUB_point = db_conn.execute(f"SELECT KP FROM Members WHERE User_ID = {message.author.id}")
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point.fetchone()
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point[0]

                REMOVED FOR GITHUB_point += 1

                db_conn.execute(f"UPDATE Members SET KP = {REMOVED FOR GITHUB_point} WHERE User_ID = {message.author.id}")
                db_conn.commit()