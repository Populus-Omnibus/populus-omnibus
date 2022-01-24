from black import lib2to3_parse
import discord
from discord.ext import commands
from datetime import datetime
from discord_slash import cog_ext, SlashContext
import interactions

import sys

sys.path.append('/home/ubuntu/server')

from filehandler import *


def get_data():
    tmpdict = (readsettings(segment="voicechannels"))
    return tmpdict

pchannel_options = [{
    "name":"channel",
    "description": "Az a voicechannel, amiből majd újabb voicechannelek képződnek",
    "required": True,
    "type": 7
}]

remove_pchannel_options = [{
    "name":"channel",
    "description": "Az a voicechannel, amit nem akarsz dinamikusnak látni",
    "required": True,
    "type": 7
}]

class voicechannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('voicechannel is ready')

    @cog_ext.cog_slash(name="add_dynamic_channel", description="Ezzel adsz hozzá dinamikus voiceot a rendszerhez", options=pchannel_options, guild_ids=[308599429122883586])
    async def set_parentchannel(self, ctx: SlashContext, channel):
        await ctx.defer(hidden=True)

        if channel.type != discord.ChannelType.voice:
            await ctx.send(content="Ez nem egy voice channel :woman_shrugging:", hidden=True)
            return

        lib = get_data()

        lib["parentchannels"].append(channel.id)
        updatesettings(segment="voicechannels", data= lib)
        await ctx.send(content=f"Saved voicechannel: {channel.name}  with ID:`{channel.id}`", hidden=True)

    @cog_ext.cog_slash(name="get_dynamic_channels", description="Az összes létező parentchannel", options=None, guild_ids=[308599429122883586])
    async def get_parentchannels(self, ctx):
        await ctx.defer(hidden = True)

        lib = get_data()

        embed = discord.Embed(
            title = "Parental voicechannels",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url= self.client.user.avatar_url)
        for x in lib["parentchannels"]:
            ch = self.client.get_channel(int(x))
            if(ch == None):
                continue
            embed.add_field(name=ch.name, value=f"Guild: {ch.guild}\n Category: {ch.category}\n Position: {ch.position}")

        await ctx.send(embed = embed, hidden = True)

    @cog_ext.cog_slash(name="remove_dynamic_channels", description="Töröl egy adott dinamikus voiceot", options=remove_pchannel_options, guild_ids=[308599429122883586])
    async def remove_parentchannel(self, ctx: SlashContext, channel):
        await ctx.defer(hidden = True)

        if channel.type != discord.ChannelType.voice:
            await ctx.send(content="Ez nem egy voice channel :woman_shrugging:", hidden=True)
            return

        lib = get_data()

        lib["parentchannels"].remove(channel.id)
        updatesettings(segment="voicechannels", data = lib)
        await ctx.send(f"Dynamic channel: {channel.name} törölve", hidden=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if(member.bot == True):
            return
        
        lib = get_data()
        parentids = lib["parentchannels"]

        #ha belép a szobát szeretnékbe
        if(after.channel !=None and after.channel.id in parentids):
            print("joined to parent channel")

            channelname = member.nick
            if member.nick == None:
                channelname = member.name
            channel = await member.guild.create_voice_channel(f"{channelname} által kért voice")
            await channel.edit(position=after.channel.position+1, category=after.channel.category, sync_permissions=True)
            await channel.set_permissions(member, manage_channels=True)
            await member.move_to(channel)

            lib["channels"].append(channel.id)

        # ha lelép a kapott szobából
        if(before.channel != None and after.channel == None):
            content = lib["channels"]
            if(len(before.channel.members)==0 and int(before.channel.id) in content):
                await before.channel.delete()
                lib["channels"].remove(int(before.channel.id))

        #ha ellép a kapott szobából
        if(before.channel != None and after.channel != None):
            content = lib["channels"]
            if(len(before.channel.members)==0 and int(before.channel.id) in content):
                await before.channel.delete()
                lib["channels"].remove(int(before.channel.id))

        updatesettings(segment="voicechannels", data = lib)


def setup(client):
    client.add_cog(voicechannel(client))
    print("voicechannel is being loaded")

def teardown(client):
    client.remove_cog(voicechannel(client))
    print("voicechannel is being unloaded")

