import discord 
from discord.ext import commands, tasks
import os
from itertools import cycle
from discord_slash import SlashCommand, SlashCommandOptionType

prefixes = []

async def get_prefix(client, message):
    if not message.guild:
        return
    return commands.when_mentioned_or(*prefixes)(client, message)

intents = discord.Intents.all()

client = commands.Bot(command_prefix = get_prefix, intents = intents, status = discord.Status.idle, activity=discord.Game(name="Booting.."))
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload = True)
status = cycle(['Rossz csatorna', 'E M B E R', 'Literálisan cringe'])
#botspam
channelids =[739567794533826616]


@client.event
async def on_ready():
		print('Karbantartás')
		print(client.user.name)
		print(client.user.id)
		print("----------")
		await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Karbantartás alatt"))
		#await client.change_presence(status=discord.Status.away, activity=discord.Activity(type=discord.ActivityType.listening, name="@vikbot"))

client.run("NzQxMDAwMDA0MTcyNTEzMzEw.XyxMCA.Rlqo4D9iswWEaXmmLbpITkBfSJQ")


