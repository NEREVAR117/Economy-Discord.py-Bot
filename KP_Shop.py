


async def KP_Prompt(message, db_conn):
    REMOVED FOR GITHUB_points = db_conn.execute('SELECT KP FROM Members WHERE User_ID = ?', (message.author.id,))
    REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points.fetchone()
    REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points[0]

    await message.channel.send("You currently have **" + str(REMOVED FOR GITHUB_points) + """KP**. You can purchase the following items:```
    [1] Kill la Kill Poster - 15kp                 (for when you wanna see those cool anime tiddies on the wall)
    [2] Naruto Headband - 25kp                     (now you, too, can be a cool ninja man)
    [3] Pikachu Shirt - 40kp                       (wear this if you both hate on pokemon games yet claim to love them)
    [4] Kirby Plushie - 60kp                       (brings you good luck and great fortune)
    [5] Waifu Pillow - 80kp                        (for all your self-exploratory, emotional, personal needs when you're alone at night)

    [6] Husbando Pillow - 90kp                     (cute anime boys have a place too)
    [7] All Might Action Figure - 120kp            (a symbol of peace to inspire you every day)
    [8] Eva Statue - 150kp                         (daily reminder of your existential crisis)
    [9] Gurren Lagann Mecha Toy - 180kp            ("Row Row Fight da Powah")
    [10] Life-like Replica of God Tongue - 250kp   (will 100% give you big food cummies)```

    Type `-kp buy [X]` where X is the item's number to purchase it. You can also type `-kp voucher` to buy a Lottery 1 ticket.""")








async def KP_Voucher(message, db_conn, time, random):

    REMOVED FOR GITHUB_points = db_conn.execute('SELECT KP FROM Members WHERE User_ID = ?', (message.author.id,))
    REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points.fetchone()
    REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points[0]

    voucher_cost = db_conn.execute('SELECT Voucher_Cost FROM Members WHERE User_ID = ?', (message.author.id,))
    voucher_cost = voucher_cost.fetchone()
    voucher_cost = voucher_cost[0]

    # Checks if the user has enough KP points
    if REMOVED FOR GITHUB_points < voucher_cost:

        await message.channel.send("You don't have enough KP points, dawg. Come back later when you have at least " + str(voucher_cost) + " points.")

    else:
        # Subtracts the KP points and iterates the voucher cost up by one
        REMOVED FOR GITHUB_points -= voucher_cost
        voucher_cost += 1

        print(REMOVED FOR GITHUB_points)

        db_conn.execute("UPDATE Members SET KP = ? WHERE User_ID = ?", (REMOVED FOR GITHUB_points, message.author.id))
        db_conn.execute("UPDATE Members SET Voucher_Cost = ? WHERE User_ID = ?", (voucher_cost, message.author.id))
        db_conn.commit()

        await message.channel.send("You bought a voucher with your KP points and exchange it for a lottery 1 ticket...")

        time.sleep(3)

        # Payout is 105% at 1.05$
        lottery_1_winnings = [*(44 * [0]), *(30 * [1]), *(20 * [2]), *(5 * [5]), *(1 * [10])]

        lottery_result = random.choice(lottery_1_winnings)

        print("Lottery-Voucher payout from " + message.author.display_name + " is:", lottery_result)

        # Adds the lottery-voucher winnings to the user money
        money = db_conn.execute('SELECT Money FROM Members WHERE User_ID = ?', (message.author.id,))
        money = money.fetchone()
        money = money[0]

        money += lottery_result

        print("Voucher-lottery added to money is", money, "ROUND THIS IF NEEDED")

        db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
        db_conn.commit()

        # Sets it to the default lottery 1 price
        what_user_paid = 1

        if lottery_result == 0:
            await message.channel.send("Oof. You got 0$ from the ticket.")

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

















async def KP_Shop(message, db_conn):
    split_message = message.content.split()

    shop_items = {'[1]': 'KLK',
                  '[2]': 'Naruto',
                  '[3]': 'Pikachu',
                  '[4]': 'Kirby',
                  '[5]': 'Waifu',
                  '[6]': 'Husbando',
                  '[7]': 'All_Might',
                  '[8]': 'Eva',
                  '[9]': 'GL_Toy',
                  '[10]': 'God_Tongue'}

    items_names = {'[1]': 'Kill la Kill poster',
                   '[2]': 'Naruto headband',
                   '[3]': 'Pikachu shirt',
                   '[4]': 'Kirby plushie',
                   '[5]': 'Waifu pillow',
                   '[6]': 'Husbando pillow',
                   '[7]': 'All Might action figure',
                   '[8]': 'Evangelion statue',
                   '[9]': 'Gurren Lagann mecha toy',
                   '[10]': '... god tongue?'}

    items_cost = {'[1]': 15,
                  '[2]': 25,
                  '[3]': 40,
                  '[4]': 60,
                  '[5]': 80,
                  '[6]': 90,
                  '[7]': 120,
                  '[8]': 150,
                  '[9]': 180,
                  '[10]': 250}

    # Check if they already own the item they're trying to buy
    print(shop_items[split_message[2]])

    item_check = db_conn.execute('SELECT (%s) FROM KP_Inventory WHERE User_ID = ?' % (shop_items[split_message[2]]), (message.author.id,))
    item_check = item_check.fetchone()
    item_check = item_check[0]

    if item_check != 'None':
        await message.channel.send("You already own that item.")

    else:
        # Checks if they even have enough KP points
        REMOVED FOR GITHUB_points = db_conn.execute('SELECT KP FROM Members WHERE User_ID = ?', (message.author.id,))
        REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points.fetchone()
        REMOVED FOR GITHUB_points = REMOVED FOR GITHUB_points[0]

        if REMOVED FOR GITHUB_points < items_cost[split_message[2]]:
            await message.channel.send("You don't have enough KP for that. Do better.")

        else:
            # Gives the user the item
            db_conn.execute("UPDATE KP_Inventory SET (%s) = ? WHERE User_ID = ?" % (shop_items[split_message[2]]), ("Owned", message.author.id))

            REMOVED FOR GITHUB_points -= items_cost[split_message[2]]

            db_conn.execute("UPDATE Members SET KP = ? WHERE User_ID = ?", (REMOVED FOR GITHUB_points, message.author.id))
            db_conn.commit()

            await message.channel.send("Yay, you got a " + str(items_names[split_message[2]]) + "!")