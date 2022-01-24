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

pchannel_options = {
    "name":"channel",
    "description": "Az a voicechannel, amiből majd újabb voicechannelek képződnek",
    "required": True,
    "type": 4
}

remove_pchannel_options = {
    "name":"channel",
    "description": "Az a voicechannel, amit nem akarsz dinamikusnak látni",
    "required": True,
    "type": 4
}

class voicechannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = get_data()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('voicechannel is ready')

    @cog_ext.cog_slash(name="addparentchannel", description="Ezzel adsz hozzá dinamikus voiceot a rendszerhez", options=pchannel_options, guild_ids=[308599429122883586])
    async def set_parentchannel(self, ctx: SlashContext, channel):
        await ctx.defer(hidden=True)

        self.data["parentchannels"].append(channel)
        updatesettings(segment="voicechannels", data= self.data)
        await ctx.send(content=f"Saved voicechannel:{channel.name}  with ID:`{channel.id}`", hidden=True)

    @cog_ext.cog_slash(name="getparentchannels", description="Az összes létező parentchannel", options=None, guild_ids=[308599429122883586])
    async def get_parentchannels(self, ctx):
        await ctx.defer(hidden = True)
        embed = discord.Embed(
            title = "Parental voicechannels",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url= self.client.user.avatar_url)
        for x in self.data["parentchannels"]:
            if(x==None):
                return
            ch = self.client.get_channel(int(x))
            embed.add_field(name=ch.name, value=f"Guild: {ch.guild}\n Category: {ch.category}\n Position: {ch.position}")

        await ctx.send(embed = embed, hidden = True)

    @cog_ext.cog_slash(name="removeparentchannels", description="Töröl egy adott voicechannelt", options=remove_pchannel_options, guild_ids=[308599429122883586])
    async def remove_parentchannel(self, ctx: SlashContext, channel):
        await ctx.defer(hidden = True)
        self.data["parentchannels"].remove(int(channel))
        updatesettings(segment="voicechannels", data = self.data)
        await ctx.send(f"Törölve channel: {channel.name}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if(member.bot == True):
            return
        
        parentids = self.data["parentchannels"]

        #ha belép a szobát szeretnékbe
        if(after.channel !=None and str(after.channel.id) in parentids):
            print("joined to parent channel")

            channelname = member.nick
            if member.nick == None:
                channelname = member.name
            channel = await member.guild.create_voice_channel(f"{channelname} által kért voice")
            await channel.edit(position=after.channel.position+1, category=after.channel.category, sync_permissions=True)
            await channel.set_permissions(member, manage_channels=True)
            await member.move_to(channel)

            self.data["parentchannels"].append(channel.id)

        # ha lelép a kapott szobából
        if(before.channel != None and after.channel == None):
            content = self.data["channels"]
            if(len(before.channel.members)==0 and int(before.channel.id) in content):
                await before.channel.delete()
                self.data["channels"].remove(int(before.channel.id))

        #ha ellép a kapott szobából
        if(before.channel != None and after.channel != None):
            content = self.data["channels"]
            if(len(before.channel.members)==0 and int(before.channel.id) in content):
                await before.channel.delete()
                self.data["channels"].remove(int(before.channel.id))

        updatesettings(segment="voicechannels", data = self.data)


def setup(client):
    client.add_cog(voicechannel(client))
    print("voicechannel is being loaded")

def teardown(client):
    client.remove_cog(voicechannel(client))
    print("voicechannel is being unloaded")

