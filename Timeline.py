


async def TimelinePrompt(message):

    await message.channel.send("""To look at the timeline for a user for comparison, use their irl name. You can do multiple users, like `-timeline REMOVED FOR GITHUB zayne`.

    For companies, you need to use their ID tags. Such as `-timeline 1 2 3`. The ID tags for each company is below:
        `[1] BDSM Planet | [2] Christian Mingle | [3] Hand-Drawn Frames Studios | [4] Honnoji Academy | [5] REMOVED FOR GITHUB Co.
        [6] Ligma Beans | [7] Military Industrial Complex | [8] National Propane Association | [9] Obama United | [10] Sorcerers of the Toast`""")







async def Timeline(message, db_conn, plt, discord):

    split_message = message.content.split()

    company_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    # First we check if the user is calling for members or a company
    print(split_message[1])
    if split_message[1] not in company_numbers:

        print("Printing users")

        split_message.pop(0)

        # Capitalizes all the names in the list
        x = 0
        for name in split_message:
            split_message[x] = split_message[x].capitalize()
            print(split_message[x])
            x += 1

        # Makes the graph bigger (default is 3, 4)
        plt.figure(figsize=(10, 8))

        # Cycles through the called username(s)
        for called_irl_name in split_message:
            member_timeline = db_conn.execute("SELECT * FROM Members_History WHERE Nickname = ?", (called_irl_name,))
            member_timeline = member_timeline.fetchall()

            # Establishes the money and date lists first to be appended
            money_timeline = []
            date_timeline = []

            # Builds a list of money and dates for the currently selected user
            for timeline_slot in member_timeline:
                money_timeline.append(float(timeline_slot[3]))

                # Formats the dates to 01-01 (removes year)
                date = timeline_slot[7]
                date = date[5:]

                date_timeline.append(date)

            # Writes the plot with circles on the points
            plt.plot(date_timeline, money_timeline, 'o-')

            # Builds onto the plot line with labeled money markers
            for x, y in zip(date_timeline, money_timeline):
                label = "{:.2f}".format(y)

                plt.annotate(label,  # this is the text
                             (x, y),  # this is the point to label
                             textcoords="offset points",  # how to position the text
                             xytext=(30, 0),  # distance from text to points (x,y)
                             ha='center')  # horizontal alignment can be left, right or center

        ax = plt.gca()

        ax.set_axisbelow(True)
        # ax.yaxis.grid(color='gray', linestyle='dashed')
        ax.xaxis.grid(color='black', linestyle='dashed')

        # plt.plot(date_timeline, money_timeline, 'ro-')
        # plt.plot(date_timeline, money_timeline)
        plt.ylabel('Net Worth $')
        plt.xlabel("Dates")
        # plt.savefig('plot.png')

        # Adds the legend to upper left corner
        plt.legend(split_message, loc='upper left')

        plt.savefig('plot.png')
        # plt.show()

        plt.clf()

        # channel = client.get_channel(REMOVED FOR GITHUB)
        await message.channel.send(file=discord.File('plot.png'))








    # Triggers if company is called instead of user(s)
    else:

        print("Printing companies")

        # Removes the -timeline part of the list message
        split_message.pop(0)

        # Sets size of the graph
        plt.figure(figsize=(10, 8))

        # Dictionary of the company names associated with specific values
        stock_companies = {'1': 'BDSM Planet', '2': 'Christian Mingle', '3': 'Hand-Drawn Frames Studios',
                           '4': 'Honnoji Academy', '5': 'REMOVED FOR GITHUB Co.', '6': 'Ligma Beans',
                           '7': 'Military Industrial Complex', '8': 'National Propane Association',
                           '9': 'Obama United', '10': 'Sorcerers of the Toast'}

        # print(stock_companies[split_message[0]])
        company_name = stock_companies[split_message[0]]
        company_names = []

        # Cycles through the called companies by their name
        for company_id in split_message:
            company_timeline = db_conn.execute("SELECT * FROM Companies_History WHERE Company_Name = ?", (stock_companies[company_id],))
            company_timeline = company_timeline.fetchall()

            # Establishes the money and date lists first to be appended
            money_timeline = []
            date_timeline = []

            # Builds a list of money and dates for the currently selected user
            for timeline_slot in company_timeline:
                money_timeline.append(float(timeline_slot[4]))

                # Formats the dates to 01-01 (removes year)
                date = timeline_slot[6]
                date = date[5:]

                date_timeline.append(date)

            # Writes the plot with circles on the points
            plt.plot(date_timeline, money_timeline, 'o-')

            # Builds onto the plot line with labeled money markers
            for x, y in zip(date_timeline, money_timeline):
                label = "{:.2f}".format(y)

                plt.annotate(label,  # this is the text
                             (x, y),  # this is the point to label
                             textcoords="offset points",  # how to position the text
                             xytext=(30, 0),  # distance from text to points (x,y)
                             ha='center')  # horizontal alignment can be left, right or center

            # Builds the list of company names for down below
            company_names.append(stock_companies[company_id])

        ax = plt.gca()

        ax.set_axisbelow(True)
        # ax.yaxis.grid(color='gray', linestyle='dashed')
        ax.xaxis.grid(color='black', linestyle='dashed')

        #         plt.plot(date_timeline, money_timeline, 'ro-')
        # plt.plot(date_timeline, money_timeline)
        plt.ylabel('Stock Value $')
        plt.xlabel("Dates")
        # plt.savefig('plot.png')

        # Adds the legend to upper left corner
        plt.legend(company_names, loc='upper left')

        plt.savefig('plot.png')
        # plt.show()

        plt.clf()

        # channel = client.get_channel(REMOVED FOR GITHUB)
        await message.channel.send(file=discord.File('plot.png'))