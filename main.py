import discord
from discord.ext import commands

import pandas as pd
import numpy as np
from os.path import exists

# initialize data file
if not exists("data.csv"):
    df = pd.DataFrame(columns = ['name', 'kills', 'credits'])
    df.to_csv("data.csv")
else: 
    df = pd.read_csv("data.csv", index_col = [0])

# Enable all intents to let the bot do anything we need it to
intents = discord.Intents.all()

# Create Client object and have all intents on
bot = discord.Client(intents = intents)


# Server role names
infector_role = 'Zombie'
team1_role = 'Pirate'
team2_role = 'Scientist'
admin_role = 'MODERATOR'

# Prints information to the terminal that the bot is running. 
@bot.event
async def on_ready():
    print('Logged on as', bot.user, 'and running.')

# A message handler to handle commands called by all players. Requires Python 3.10 to run. 
@bot.event
async def on_message(message: discord.Message):
    # If it is not in a server ignore the message (NO DM'S)
    if message.guild is None:
        return 

    # Bot doesn't respond to itself
    if message.author == bot.user:
        return

    #read messages and check the first 8 characters for matching a command
    match message.content[0:8]:
        case '!addkill':
            # call addkill utility function
            await addKill(message)
            return
        case '!dispute':
            # call dispute utility function
            admins = discord.utils.get(message.guild.roles, name = admin_role).members
            for admin in admins:
                await admin.send(f"Player {message.author.name} has disputed an action by another player. Contact {message.author.name} for more information")
            return
        case '!usrhelp':
            # send a message to the author through DM's to explain commands
            await message.author.send(f"Hello!\nThe following commands are available through server chats:\n\n!addkill @user1 @user2 ...\nThis command reports kills you have made in the game and updates your stats\n\n!dispute\nThis command reports to mods that you want to dispute your status in the game (e.g. you were reported killed but you weren't, etc.)\n\n!usrhelp\nThis command tells you what commands are available. If you're not sure, you can always ask.\n\n!mystats\nThis command will print out your kills and your current credits.")
            return
        case '!addcred':
            # use addCred utility only if user is admin
            if discord.utils.get(message.author.roles, name = admin_role) is None:
                await message.author.send("You do not have permission to call this command.")
                return
            else:
                await addCred(message)
            return
        case '!remcred':
            # use remcred utility only if user is admin
            if discord.utils.get(message.author.roles, name = admin_role) is None:
                await message.author.send("You do not have permission to call this command.")
                return
            else:
                await remCred(message)
            return
        case '!mystats':
            # call mystats utility to view your kills and credits. 
            await myStats(message)
            return

# An event handler for when new people join the HvZ Discord Server
@bot.event
async def on_member_join(member):
    await member.send(f'Hello {member.name} and welcome to the Nerf@Noyce Discord server!')

# Command that players can call when they've killed another player
async def addKill(message: discord.Message):
    # find killed list and check if it is empty
    killed = message.mentions
    if not killed:
        await message.channel.send("Usage is '!addkill @player1 @player2 ....")
    
    # Don't let the author kill themselves
    if message.author in killed:
        await message.author.send("WARNING: You cannot kill yourself.")
        return

    # If the author hasn't been added to dataframe (first entry) add them
    if message.author.name not in df['name'].values:
        df.loc[len(df.index)] = [message.author.name, 0, 0]
    
    lst = df.index[df['name'] == message.author.name].tolist()
    index = lst[0]

    # If the killer was a zombie
    if discord.utils.get(message.author.roles, name = infector_role) is not None:

        for x in killed:
            # case where a zombie "kills" another zombie, and nothing should happen
            # because it was probably a mistake
            if discord.utils.get(x.roles, name = infector_role) is not None:
                await x.send(f"{message.author.name} 'killed' you, but you both were already zombies. Carry on like nothing happened, or contact a mod if you have a question.")
                df.to_csv("data.csv") 
                return

            # write to dataframe
            df.at[index, 'kills'] += 1
            # message to tell victim they've been killed
            await x.send(f"Oh no, you've been zombified by {message.author.name}! \nContact a mod if you have a question. If you want to dispute this, use !dispute.")

            # The chunk below should change the role of the victim to a zombie, and remove the other roles. 
            added = discord.utils.get(message.guild.roles, name = infector_role)
            removed1 = discord.utils.get(message.guild.roles, name = team1_role)
            removed2 = discord.utils.get(message.guild.roles, name = team2_role)
            await discord.Member.add_roles(x, added)
            await discord.Member.remove_roles(x, *[removed1,removed2])
    else: 
        # If someone from team1 kills someone else, and if someone from team2 kills someone else.
        for x in killed:
            if discord.utils.get(message.author.roles, name = team1_role) is not None:
                if discord.utils.get(x.roles, name = team1_role) is None:
                    df.at[index, 'kills'] += 1
                    await x.send(f"Oh no! {message.author.name} from {team1_role} killed you! \nContact a mod if you have a question. If you want to dispute this, use !dispute.")
                    
            if discord.utils.get(message.author.roles, name = team2_role) is not None:
                if discord.utils.get(x.roles, name = team2_role) is None:
                    df.at[index, 'kills'] += 1
                    await x.send(f"Oh no! {message.author.name} from {team2_role} killed you! \nContact a mod if you have a question. If you want to dispute this, use !dispute.")    

    df.to_csv("data.csv")

# Command that players can call when they've killed another player
async def addCred(message: discord.Message):
    # Find who was mentioned and what role
    credited = message.mentions
    credrole = message.role_mentions
    print(credrole)
    
    # nothing input
    if not credited and not credrole:
        await message.channel.send("Usage is '!addcred @player1 @player2 ....")
        return
    
    # For all the roles mentioned and all members of that role, give them a credit
    for role in credrole:
        for x in role.members:
            await x.send("You received one (1) credit from your team's spoils! Spend it wisely...")
            #update datatframe
            if x.name in df['name'].values:
                lst = df.index[df['name'] == x.name].tolist()
                index = lst[0]
                df.at[index, 'credits'] += 1
            else:
                df.loc[len(df.index)] = [x.name, 0, 1]

    # For all people mentioned, give them a credit
    for x in credited:
        await  x.send("You received one (1) credit! Spend it wisely...")
        #update dataframe
        if x.name in df['name'].values:
            lst = df.index[df['name'] == x.name].tolist()
            index = lst[0]
            df.at[index, 'credits'] += 1
        else:
            df.loc[len(df.index)] = [x.name, 0, 1]
    #write to dataframe
    df.to_csv("data.csv") 
    return

# This function shall be called only by a moderator when a player spends credits for anything. 
# NOTE: This function, unlike addCred, will take only one player and an amount that they spent. 
async def remCred(message: discord.Message):
    credited = message.mentions
    if not credited or len(credited) > 1:
        await message.channel.send("Usage is '!remcred @player x")
        return

    fields = message.content.split()
    spent = int(fields[2])

    if spent <= 0:
        await message.author.send("Spent amount should be a strictly positive, nonzero integer")
        return
    
    name = credited[0].name
    if name in df['name'].values:
        lst = df.index[df['name'] == name].tolist()
        index = lst[0]
        if df.at[index, 'credits'] >= spent:
            df.at[index, 'credits'] -= spent
        else:
            await message.author.send("{name} does not have the credits to process this transaction")
            return
    else:
        await message.author.send("{name} has no credits available for this transaction")
        df.loc[len(df.index)] = [name, 0, 0]
    df.to_csv("data.csv") 
    return

# This function shall have the bot PM the caller of this function to show them their kills and credits. 
async def myStats(message: discord.Message):
    if message.author.name in df['name'].values:
        lst = df.index[df['name'] == message.author.name].tolist()
        index = lst[0]
        await message.author.send(f"You have:\n{df.at[index, 'kills']} kill(s)\n{df.at[index, 'credits']} credit(s)")
    else:
        await message.author.send(f"You have:\n0 kills\n0 credits")
    return

intents = discord.Intents.default()
bot.run('OTY3ODY4NjQ4NzEyNzIwMzk0.YmWj6w.PtQxS-Qh3kETdnGH9BpA51dfdMI')