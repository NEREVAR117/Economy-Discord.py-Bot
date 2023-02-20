


async def ShopPrompt(message):
    # Prompts for the shop sub-functions
    await message.channel.send("""You can purchase the following items:
```    [1] Black ski mask - 20$        (for skiing and nothing else, totally doesn't make you harder to identify)
    [2] Nice resume - 50$           (a good resume helps you find better jobs and earn more income)
    [3] Quality haircut - 120$     (improves your income earnings, makes you slightly more likeable)
    [4] Pistol - 450$                     (reduces your chance of being robbed)
    [5] Nice suit - 1,200               (improves your income earnings, makes you slightly more likely to be robbed)
    [6] Car - 25,000                     (improves your income earnings, makes you much harder to be robbed)
    [7] Accountant - 80,000      (improves your income earnings)```

    Type `-shop buy [X]` where X is the item's number to purchase it.""")




async def Shop(message, db_conn):
    # Actually lets people buy from the shop
    split_message = message.content.split()

    shop_items = {'[1]': 'Mask',
                  '[2]': 'Resume',
                  '[3]': 'Haircut',
                  '[4]': 'Gun',
                  '[5]': 'Suit',
                  '[6]': 'Car',
                  '[7]': 'Accountant'}

    items_cost = {'[1]': 20,
                  '[2]': 50,
                  '[3]': 120,
                  '[4]': 450,
                  '[5]': 1200,
                  '[6]': 25000,
                  '[7]': 80000}

    # Check if they already own the item they're trying to buy
    print(shop_items[split_message[2]])

    item_check = db_conn.execute('SELECT (%s) FROM Inventory WHERE User_ID = ?' % (shop_items[split_message[2]]), (message.author.id,))
    item_check = item_check.fetchone()
    item_check = item_check[0]

    if item_check != 'None':
        await message.channel.send("You already own that item.")

    else:
        # Checks if they even have enough money
        money = db_conn.execute('SELECT Money FROM Members WHERE User_ID = ?', (message.author.id,))
        money = money.fetchone()
        money = money[0]

        if money < items_cost[split_message[2]]:
            await message.channel.send("You don't have enough money for that, you poor bitch.")

        else:
            # Gives the user the item
            db_conn.execute("UPDATE Inventory SET (%s) = ? WHERE User_ID = ?" % (shop_items[split_message[2]]), ("Owned", message.author.id))

            money -= items_cost[split_message[2]]

            db_conn.execute("UPDATE Members SET Money = ? WHERE User_ID = ?", (money, message.author.id))
            db_conn.commit()

            if shop_items[split_message[2]] == 'Kirby':
                karma = db_conn.execute('SELECT Karma FROM Members WHERE User_ID = ?', (message.author.id,))
                karma = karma.fetchone()
                karma = karma[0]

                karma += 1

                db_conn.execute("UPDATE Members SET Karma = ? WHERE User_ID = ?", (karma, message.author.id))
                db_conn.commit()

                await message.channel.send(
                    "Yay, you got a " + str(shop_items[split_message[2]]).lower() + "!\n https://www.icegif.com/wp-content/uploads/icegif-59.gif")

            else:
                await message.channel.send("Yay, you got a " + str(shop_items[split_message[2]]).lower() + "!")

                # Adds a KP point to the user
                REMOVED FOR GITHUB_point = db_conn.execute(f"SELECT KP FROM Members WHERE User_ID = {message.author.id}")
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point.fetchone()
                REMOVED FOR GITHUB_point = REMOVED FOR GITHUB_point[0]

                REMOVED FOR GITHUB_point += 1

                db_conn.execute(f"UPDATE Members SET KP = {REMOVED FOR GITHUB_point} WHERE User_ID = {message.author.id}")
                db_conn.commit()