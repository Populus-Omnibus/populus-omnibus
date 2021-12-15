import discord
import os
from discord.ext import commands
from discord_slash import SlashCommand
import json
from datetime import datetime

prefixes = []
channelids = []

with open("settings/main_settings.json", "r") as fp:
    tempdict = json.loads(fp.read())
    prefixes = tempdict["prefixes"]
    channelids = tempdict["channels"]
    print("Settings loaded")

async def get_prefix(client, message):
    if not message.guild:
        return
    return commands.when_mentioned_or(*prefixes)(client, message)

intents = discord.Intents.all()

client = commands.Bot(command_prefix = get_prefix, intents = intents, status = discord.Status.idle, activity=discord.Game(name="Booting..."))

slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload = True)

@client.event
async def on_ready():
		print('Lets rock!')
		print(client.user.name)
		print(client.user.id)
		print(client.guilds)
		print("----------")
		await client.change_presence(activity=discord.Activity(name='Duck Hunt', type=5, details="doing some shit", large_image_url="https://imgur.com/lEquJkV"))

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

def save_settings():
    tempdict["prefixes"] = prefixes
    tempdict["channels"] = channelids
    with open("settings/main_settings.json", "w") as fp:
        json.dump(tempdict, fp)
    print("Prefixes saved")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.channel.id in channelids or message.author.id == 297689894208274432:
            await client.process_commands(message)

@client.event
async def on_command_error(ctx, errors):
    await ctx.send(errors)

@client.command()
async def ping(ctx):
    await ctx.send(f'{client.latency}')
    
@client.command(description='Kills the bot')
async def kys(ctx):
    if ctx.author.id == 297689894208274432:
        await ctx.channel.send("Going back to vietnam")
        await client.logout()
        exit()
    else: await ctx.channel.send("You jerk!")

@client.command(brief='Cognevek listája fájlnév szerint.')
async def coglist(ctx):
    lista = '```'
    for x in os.listdir('./cogs'):
        if x.endswith('.py'):
            lista = lista + x[:-3] + " "
    lista += "```"
    cogs = commands.Bot.cogs
    await ctx.channel.send(f"{lista}\n{cogs}")

@client.group()
async def prefix(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid command passed...')

@prefix.command()
async def add(ctx, prefix):
    global prefixes
    if prefix in prefixes:
        await ctx.channel.send('Már létezik, te literális majom! :rofl:')
    else:
        prefixes.append(prefix)
        await ctx.channel.send(f'Added `{prefix}` to the prefix list. :ok_hand:')
        save_settings()

@prefix.command()
async def remove(ctx, prefix):
    if prefix in prefixes:
        prefixes.remove(prefix)
        await ctx.channel.send(f'Removed `{prefix}` from the prefix list.')
        save_settings()
    else:
        await ctx.channel.send('Nincs ilyen prefix! :angry::anger:')

@prefix.command()
async def list(ctx):
    await ctx.channel.send(f'```{prefixes}```')

@client.group(aliases=["cc"])
async def commandchannel(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid command passed...')

@commandchannel.command()
async def add(ctx, channelid: int):
    if channelid in channelids:
        await ctx.channel.send('Már létezik, te literális majom! :rofl:')
    else:
        channelids.append(channelid)
        await ctx.channel.send(f'Added `{channelid}` to the command channel list. :ok_hand:')
        save_settings()

@commandchannel.command()
async def remove(ctx, channelid: int):
    if channelid in channelids:
        channelids.remove(channelid)
        await ctx.channel.send(f'Removed `{channelid}` from the command channel list.')
        save_settings()
    else:
        await ctx.channel.send('Nincs ilyen channel! :angry::anger:')

@commandchannel.command()
async def list(ctx):
    embed = discord.Embed(
        title = "Command channels",
        colour = discord.Colour.blue(),
        timestamp = datetime.utcnow()
    )
    embed.set_thumbnail(url = client.user.avatar_url)
    for x in channelids:
        ch = client.get_channel(int(x))
        if(ctx.channel.guild.id == ch.guild.id):
            embed.add_field(name=ch.name, value=f"Id: {x}\n Guild: {ch.guild}\n Category: {ch.category}\n Position: {ch.position}")

    await ctx.send(embed = embed)

client.run("NzQxMjAxNzg2NjA1NDA0MTgw.Xy0H9A.U5CE2BHFoq0Z60Xsk5-I4CaBnLc")

