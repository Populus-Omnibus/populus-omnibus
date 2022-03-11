from os import nice
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import json
import os.path
from os import path

reacc_role_opt = [{
    "name":"msg",
    "description": "Üzenet id-je amin a reacc van",
    "required": True,
    "type": 3
},
{
    "name":"reacc_role",
    "description": "Role amit adni kell",
    "required": True,
    "type": 8
}]

class reaccrole(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('reaccrole is ready')

    @commands.command()
    async def testcog_reaccrole(self, ctx):
        await ctx.send("Cog is ready")

    @cog_ext.cog_slash(name = "reacc_role", description="Reaction role", options=reacc_role_opt, guild_ids=[308599429122883586, 642814459051638807])
    async def _add_reacc_role(self, ctx: SlashContext, msg: int, reacc_role: discord.Role):
        await ctx.defer(hidden=True)

        tmpdict = {"msg_id": int(msg), "role_id" : int(reacc_role.id), "done": None}

        with open(f"/home/ubuntu/bots/vikbot/jh/{msg}.json", "w") as fp:
            fp.write(json.dumps(tmpdict))

        await ctx.send(content=f"```json\n{tmpdict}\n```", hidden=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        if (os.path.exists(f"/home/ubuntu/bots/vikbot/jh/{payload.message_id}.json") == False):
            return

        tmpdict = None
        with open(f"/home/ubuntu/bots/vikbot/jh/{payload.message_id}.json", "r") as fp:
            tmpdict = json.loads(fp.read())

        if tmpdict["done"] == None and tmpdict["msg_id"] == payload.message_id:
            await msg.add_reaction(payload.emoji)
            tmpdict["emoji"] = payload.emoji.name
            tmpdict["done"] = True
            with open(f"/home/ubuntu/bots/vikbot/jh/{payload.message_id}.json", "w") as fp:
                fp.write(json.dumps(tmpdict))

        if(member == self.client.user or member.bot == True):
            return

        roles = member.guild.roles
        addedrole = None
        for role in roles:
            if role.id == int(tmpdict["role_id"]):
                addedrole = role

        if(tmpdict["emoji"] == payload.emoji.name and int(tmpdict["msg_id"]) == payload.message_id):
            await member.add_roles(addedrole)
        

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        
        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        if (os.path.exists(f"/home/ubuntu/bots/vikbot/jh/{payload.message_id}.json") == False):
            return

        if(member == self.client.user or member.bot == True):
            return

        tmpdict = None
        with open(f"/home/ubuntu/bots/vikbot/jh/{payload.message_id}.json", "r") as fp:
            tmpdict = json.loads(fp.read())

        roles = member.guild.roles
        rmdrole = None
        for role in roles:
            if role.id == int(tmpdict["role_id"]):
                rmdrole = role

        if(tmpdict["emoji"] == payload.emoji.name and int(tmpdict["msg_id"]) == payload.message_id):
            await member.remove_roles(rmdrole)

def setup(client):
    client.add_cog(reaccrole(client))
    print("reaccrole is being loaded")

def teardown(client):
    client.remove_cog(reaccrole(client))
    print("reaccrole is being unloaded")