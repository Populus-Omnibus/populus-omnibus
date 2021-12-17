from os import write
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import uuid
import urllib.request, json 

from server.filehandler import readsettings as read
from server.filehandler import updatesettings as write

from server.updater import function as tester, servertester

auth_options = [
    {
        "name":"token",
        "description":"Ezzel a tokennel csatlakozol a szerverhez",
        "required": True,
        "type":3
    },
    {
        "name":"displayname",
        "description":"Ez a név lesz látható mások számára a szerveren",
        "required": True,
        "type":3
    }
]

class mcauth(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('mcauth is ready')

    @commands.command()
    async def testcog_mcauth(self, ctx):
        await ctx.send("Cog is ready")

    @cog_ext.cog_slash(name="token", description="Megmutatja a regisztrált tokent", options=None, guild_ids=[308599429122883586])
    async def token_slash(self, ctx: SlashContext):
        await ctx.defer(hidden=True)
        tmpdict = json.loads(read(segment="mc_acc"))
        token = tmpdict[str(ctx.author.id)]["token"]
        dpname = tmpdict[str(ctx.author.id)]["displayname"]
        await ctx.send(content=f"Token: {token} | Displayname: {dpname}", hidden=True)

    @cog_ext.cog_slash(name="mcauth", description="Nem eredetis játékosok ezzel tudnak karaktert regisztrálni", options=auth_options, guild_ids=[308599429122883586])
    async def mcauth_slash(self, ctx: SlashContext, token, displayname):
        await ctx.defer(hidden=True)
        tmpdict = json.loads(read(segment="mc_acc"))
        accountdict = {}

        accountdict["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, token))
        accountdict["token"] = token
        accountdict["displayname"] = displayname

        if str(ctx.author.id) in list(tmpdict.keys()):
            accountdict["id"] = tmpdict[str(ctx.author.id)]["id"]

        for id in tmpdict:
            if tmpdict[id]["token"] == token or tmpdict[id]["displayname"] == token or tmpdict[id]["token"] == displayname or tmpdict[id]["displayname"] == displayname:
                await ctx.send(content="A `token` és `displayname` nem egyezhet két offline játékos között", hidden=True)
                return

        with urllib.request.urlopen(f"https://api.mojang.com/users/profiles/minecraft/{displayname}") as url1:
            getname = url1.read().decode()

        with urllib.request.urlopen(f"https://api.mojang.com/users/profiles/minecraft/{token}") as url2:
            gettoken = url2.read().decode()

        if gettoken == "" and getname == "" and token!= displayname :
                tmpdict[str(ctx.author.id)] = accountdict
                write(segment="mc_acc", data=tmpdict)
                await ctx.send(content="Saved account", hidden=True)
                print("saved new user")
        else:
            await ctx.send(content="Nem használhatsz online accountot `token`-ként és `displayname`-ként. A `token` és `displayname` nem egyezhet. :triumph:", hidden=True)

    @commands.command()
    async def start_server(self, ctx):
        servertester()

def setup(client):
    client.add_cog(mcauth(client))

