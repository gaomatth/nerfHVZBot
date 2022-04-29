import discord
from discord.ext import commands

import pandas as pd
import numpy as np

# Enable all intents to let the bot do anything we need it to
intents = discord.Intents.all()

# Create Client object and have all intents on
bot = discord.Client(intents = intents)

# Prints information to the terminal that the bot is running. 
@bot.event
async def on_ready():
    print('Logged on as', bot.user, 'and running.')

# A placeholder message handler.
@bot.event
async def on_message(message: discord.Message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    
    match message.content[0:7]:
        case '!addkill':
            return
        case '!dispute':
            return
        case '!plshelp':
        case '!joingrp':

        
        

    # Pseudocode below:
    # This command should separate the string into fields, and returns nothing
    # Each field should be the ID of another player in the Discord server
    # For each field: 
    #   increment the kills count field in the dataframe (csv file) using Pandas for the player who called the command
    #   Check if the player calling the command was a zombie:
    #       If check_zombie returns True, change the role of each field ID (player who was killed) to a zombie


# An event handler for when new people join the HvZ Discord Server
@bot.event
async def on_member_join(member):
    await member.send(f'Hello {member.name} and welcome to the Nerf@Noyce Discord server! [Rules TBD]. ')

# Command that players can call when they've killed another player

# This is a helper function called by other commands
def check_zombie(player):
    return True
    # Pseudocode below:
    # Check if player has the zombie role, return True if it is
    # If not, return false

def addKill(message: discord.Message):
    killed = message.mentions
    if len(killed) <= 0:
        message.channel.send("Usage is '!addkill @player1 @player2 ....")
    auth_roles = message.author.roles
    role_str = []
    for x in auth_roles:
        role_str.append(x.name)
    if 'cadmin' in role_str:
        for x in killed:
            

intents = discord.Intents.default()
bot.run('OTY3ODY4NjQ4NzEyNzIwMzk0.YmWj6w.lMTKMFzaT9ItHTCWiWJFEOvm_wI')