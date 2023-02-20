# Created on June 17th, 2021. Improved calling for a user's piechart. Put into its own file (removed from main file)







async def PiechartPrompt(message):
    await message.channel.send("Type either `-piechart server` to see a generalized server piechart, or type `-piechart (irl name)` to see that person's piechart.")


async def Piechart(message, db_conn, plt, discord):
    split_message = message.content.split()

    # If server is specified
    if split_message[1] == 'server':

        # Gets all current member data
        server_money = db_conn.execute("SELECT * FROM Members")
        server_money = server_money.fetchall()

        # Gets the total net worth of the server right now
        total_net_worth = 0
        for net_worth in server_money:
            total_net_worth += net_worth[3]

        print("Total net worth is", total_net_worth)

        # Gets the percentages for each user
        net_worth_percentage = []
        for net_worth in server_money:
            net_worth_percentage.append(round(net_worth[3] / total_net_worth * 100, 2))

        print("Sum of percentages should be 100, it is currently:", sum(net_worth_percentage))

        # Combines the user name with their money value
        name_and_net_worth = []
        for user in server_money:
            name_and_value = str(user[2]) + " - "
            name_and_value += str(user[3]) + "$"

            name_and_net_worth.append(name_and_value)

        # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        # sizes = [15, 30, 45, 10]
        # explode = (0, 0.2, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        # Makes the graph bigger (default is 3, 4)
        plt.figure(figsize=(10, 10))

        fig1, ax1 = plt.subplots()
        ax1.pie(net_worth_percentage, labels=name_and_net_worth, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        ax1.set_title("Server Total Users", fontsize=20)

        plt.savefig('pie.png')
        # plt.show()

        plt.clf()

        # channel = client.get_channel(REMOVED FOR GITHUB)
        await message.channel.send(file=discord.File('pie.png'))






    # If the server isn't specified (instead checking a user)
    else:

        irl_name = split_message[1]
        irl_name = irl_name.capitalize()

        # Gets all current member data from chosen irl name
        user_profile = db_conn.execute("SELECT * FROM Members WHERE Nickname = ?", (irl_name,))
        user_profile = user_profile.fetchone()

        # We assign the data to easily readable and useable variable names
        net_worth = user_profile[3]
        money = user_profile[4]
        bank = user_profile[5]
        stock_value = user_profile[6]

        # We compile a list of the relevant number data for the piechart
        member_data = []
        member_data.append(money)
        member_data.append(bank)
        member_data.append(stock_value)

        # We compile a list of the relevant number data's labels so the piechart's information is actually readable
        member_data_labels = []
        member_data_labels.append("Money - " + str(money) + "$")
        member_data_labels.append("Bank - " + str(bank) + "$")
        member_data_labels.append("Stocks Value - " + str(stock_value) + "$")

        # Sets the image size
        plt.figure(figsize=(10, 10))

        # Plot library functions / logic
        fig1, ax1 = plt.subplots()
        ax1.pie(member_data, labels=member_data_labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Title of the pie chart
        ax1.set_title(irl_name + "'s Net Worth: " + str(net_worth) + "$", fontsize=20)

        plt.savefig('pie.png')
        # plt.show()

        plt.clf()

        await message.channel.send(file=discord.File('pie.png'))