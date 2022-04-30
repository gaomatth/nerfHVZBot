import discord
from discord.ext import commands

import pandas as pd
from os.path import exists

if not exists("data.csv"):
    df = pd.DataFrame(columns = ['name', 'kills', 'credits'])
    df.to_csv("data.csv")
else: 
    df = pd.read_csv("data.csv")

# Enable all intents to let the bot do anything we need it to
intents = discord.Intents.all()

# Create Client object and have all intents on
bot = discord.Client(intents = intents)

infector_role = 'cadmin'
team1_role = 'badmin'
team2_role = 'badmin'
admin_role = 'Admin'
# Prints information to the terminal that the bot is running. 
@bot.event
async def on_ready():
    print('Logged on as', bot.user, 'and running.')

# A placeholder message handler.
@bot.event
async def on_message(message: discord.Message):
    # don't respond to ourselves
    if message.guild is None:
        return 
    if message.author == bot.user:
        return

    match message.content[0:8]:
        case '!addkill':
            await addKill(message)
            return
        case '!dispute':
            admins = discord.utils.get(message.guild.roles, name = admin_role).members
            for admin in admins:
                await admin.send(f"Player {message.author.name} has disputed an action by another player. Contact {message.author.name} for more information")
            return
        case '!usrhelp':
            await message.author.send(f"Hello!\nThe following commands are available through server chats:\n\n!addkill @user1 @user2 ...\nThis command reports kills you have made in the game and updates your stats\n\n!dispute\nThis command reports to mods that you want to dispute your status in the game (e.g. you were reported killed but you weren't, etc.)\n\n!usrhelp\nThis command tells you what commands are available. If you're not sure, you can always ask.\n\n!mystats\nThis command will print out your kills and your current credits.")
            return
        case '!addcred':
            if discord.utils.get(message.author.roles, name = admin_role) is None:
                return
            else:
                await addCred(message)
            return
        case '!remcred':
            if discord.utils.get(message.author.roles, name = admin_role) is None:
                return
            else:
                await remCred(message)
            return
        case '!mystats':
            return

# An event handler for when new people join the HvZ Discord Server
@bot.event
async def on_member_join(member):
    await member.send(f'Hello {member.name} and welcome to the Nerf@Noyce Discord server! [Rules TBD]. ')

@bot.event
async def on_disconnect():
    df.to_csv("data.csv")
    await bot.close()

# Command that players can call when they've killed another player
async def addKill(message: discord.Message):
    killed = message.mentions
    if killed is None:
        message.channel.send("Usage is '!addkill @player1 @player2 ....")
    
    if message.author in killed:
        await message.author.send("WARNING: You cannot kill yourself.")
        return

    if message.author.name in df['name'].values:
        lst = df.index[df['name'] == message.author.name].tolist()
        index = lst[0]
        df.at[index, 'kills'] += len(killed)
    else:
        df.loc[len(df.index)] = [message.author.name, len(killed), 0]

    # If the killer was a zombie
    if discord.utils.get(message.author.roles, name = infector_role) is not None:
        for x in killed:
            # case where a zombie "kills" another zombie, and nothing should happen
            # because it was probably a mistake
            if discord.utils.get(x.roles, name = infector_role) is not None:
                await x.send(f"{message.author.name} 'killed' you, but you both were already zombies. Carry on like nothing happened, or contact a mod if you have a question.")
                return
                
            # EDIT MESSAGE TO REFLECT ROLE NAMES
            await x.send(f"Oh no, you've been cadminned by {message.author.name}! \nContact a mod if you have a question. If you want to dispute this, use !dispute.")

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
                    await x.send(f"Oh no! {message.author.name} from Team {team1_role} killed you! \nContact a mod if you have a question. If you want to dispute this, use !dispute.")
                    return
            if discord.utils.get(message.author.roles, name = team2_role) is not None:
                if discord.utils.get(x.roles, name = team2_role) is None:
                    await x.send(f"Oh no! {message.author.name} from Team {team2_role} killed you! \nContact a mod if you have a question. If you want to dispute this, use !dispute.")
                    return

# Command that players can call when they've killed another player
async def addCred(message: discord.Message):
    print("!addcred to be implemented")
    return

                    
async def remCred(message: discord.Message):
    print("!remcred to be implemented")
    return

intents = discord.Intents.default()
bot.run('OTY3ODY4NjQ4NzEyNzIwMzk0.YmWj6w.lMTKMFzaT9ItHTCWiWJFEOvm_wI')