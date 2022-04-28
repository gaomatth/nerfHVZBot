import discord
import pandas as pd
import numpy as np

# Enable all intents to let the bot do anything we need it to
intents = discord.Intents.all()

# Create Client object and have all intents on
client = discord.Client(intents = intents)

# Prints information to the terminal that the bot is running. 
@client.event
async def on_ready():
    print('Logged on as', client.user, 'and running.')

# A placeholder message handler.
@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return

    if message.content == 'ping':
        await message.channel.send('pong')

# An event handler for when new people join the HvZ Discord Server
@client.event
async def on_member_join(member):
    await member.send(f'Hello {member.name} and welcome to the HvZ Discord server! [Rules TBD]. ')

# Command that players can call when they've killed another player
@client.command
async def add_kill(message):
    # Pseudocode below:
    # This command should separate the string into fields, and returns nothing
    # Each field should be the ID of another player in the Discord server
    # For each field: 
    #   increment the kills count field in the dataframe (csv file) using Pandas for the player who called the command
    #   Check if the player calling the command was a zombie:
    #       If check_zombie returns True, change the role of each field ID (player who was killed) to a zombie
    return None

# This is a helper function called by other commands
def check_zombie(player):
    return True
    # Pseudocode below:
    # Check if player has the zombie role, return True if it is
    # If not, return false
    



intents = discord.Intents.default()
client.run('OTY3ODY4NjQ4NzEyNzIwMzk0.YmWj6w.lMTKMFzaT9ItHTCWiWJFEOvm_wI')