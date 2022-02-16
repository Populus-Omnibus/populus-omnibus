import discord
from discord.enums import ContentFilter
from discord.ext import commands
from discord_slash import client, cog_ext, SlashContext
from discord_slash.context import ComponentContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import asyncio
import json

gm_roles = [
    "740528491367497781", #1. mc
    "796695732740554764", #2. csgo
    "796695564024283156", #3. lol
    "796696220286058516", #4. r6
    "796696319640993812", #5. amogus
    "894182437897244683", #6. rocket league
    "894183010759507978", #7. overwatch
    "894181680875712572", #8. apex
    "942007674973847622", #9. factorio
    "942008102545408000", #10. civ
    "942009855265366017", #11. dont starve
    "942010109800886273", #12. terraria
    "942010273420693534", #13. space eng.
    "942010547799482409" #14. sakk
    ]

ping_roles = [
    "942033741809844254", #heti funky
    "884713029105766490", # játszóház
    "940647408247930880", #sem
    "889185131909226546", #lanosch
    "744652294150291477", #senior
    "942069245649489920", #ha5kdu
    "942073791788498974", #heti vikes
    "942119949957214280" #joker
]

gm_select = None
year_select = None
szak_select = None
faction_select = None
ping_select = None

with open("/home/ubuntu/bots/testbot/settings/roles/gm_roles.json", "r") as fp:
    gm_select = json.loads(fp.read())

with open("/home/ubuntu/bots/testbot/settings/roles/year_roles.json", "r") as fp:
    year_select = json.loads(fp.read())

with open("/home/ubuntu/bots/testbot/settings/roles/szak_roles.json", "r") as fp:
    szak_select = json.loads(fp.read())

with open("/home/ubuntu/bots/testbot/settings/roles/faction_roles.json", "r") as fp:
    faction_select = json.loads(fp.read())

with open("/home/ubuntu/bots/testbot/settings/roles/ping_roles.json", "r") as fp:
    ping_select = json.loads(fp.read())

class slash_command_support(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler()
        self.joblist=[]
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('slashcog is ready')
        self.scheduler.start()

    @commands.command()
    async def testcog_slashcommands(self, ctx):
        await ctx.send("Cog is ready")

    async def cooldowntimer(self, name):
        print("Job done")
        for x in self.joblist:
            if x.id == name:
                self.joblist.remove(x)

    ping_options = [
        {
            "name":"joke",
            "description":"Joke része a dolognak",
            "required": False,
            "type":5
        }
    ]

    @cog_ext.cog_slash(name="ping", description = "Tells you the ping", guild_ids = [308599429122883586, 737284142462402560], options = ping_options)
    async def test(self, ctx: SlashContext, joke = True):
        #await ctx.defer()
        if(joke):
            await ctx.send(content = "Pong!", hidden= False)
        else:
            await ctx.send(content=f"A ping az {round(self.client.latency*1000)}ms", hidden= True)

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        await ctx.defer(hidden=True)

        if ctx.component_type == 2:
            return
        
        for x in self.joblist:
            if x.id == str(ctx.author.name):
                await ctx.send(f"Még várj ennyi időegységet(másodpercet) légyszi: {str((x.next_run_time)-pytz.utc.localize(datetime.now()))[14:-7]}", hidden=True)
            return

        roles = ctx.author.guild.roles
        member_roles = ctx.author.roles

        """if "Évfolyam: " in ctx.values[0]:
            for x in ctx.author.roles:
                if "Évfolyam: " in str(x.name):
                    await ctx.author.remove_roles(x)
            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)

        if "Gárda: " in ctx.values[0]:
            for x in ctx.author.roles:
                if "Gárda: " in str(x.name):
                    await ctx.author.remove_roles(x)
            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)

        if "Szak: " in ctx.values[0]:
            for x in ctx.author.roles:
                if "Szak: " in str(x.name):
                    await ctx.author.remove_roles(x)
            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)

        await ctx.send(f"Ezt választottad: {ctx.values[0]}", hidden=True)"""

        selected_roles = discord.Embed(title = "Választott role(ok)",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow())

        for role in roles:
            if str(role.id) in ctx.values:
                await ctx.author.add_roles(role)      
                selected_roles.add_field(name=f"**{role.name}**", value=f"{role.mention}")

        if ctx.custom_id == "gm_select":
            for m_role in member_roles:
                if str(m_role.id) in gm_roles and str(m_role.id) not in ctx.values:
                    await ctx.author.remove_roles(m_role)

        if ctx.custom_id == "ping_select":
            for m_role in member_roles:
                if str(m_role.id) in ping_roles and str(m_role.id) not in ctx.values:
                    await ctx.author.remove_roles(m_role)

        await ctx.send(embed=selected_roles, hidden=True)

        thisjob = self.scheduler.add_job(self.cooldowntimer, run_date=(datetime.now())+timedelta(seconds=5), id=f"{ctx.author.name}", args=[ctx.author.name])
        print(str((datetime.now())+timedelta(seconds=5)))
        self.joblist.append(thisjob)
    
    """@commands.Cog.listener()
    async def on_member_update(self, before, after):
        roles = await after.guild.fetch_roles()
        for x in roles:
            if str(x.name) =="Generic évfolyam":
                givenrole = x

        for x in after.roles:
            if "Évfolyam: " in x.name:
                await after.add_roles(givenrole)
                return"""

    @cog_ext.cog_slash(name="year_select", guild_ids=[308599429122883586, 737284142462402560], options=None)
    async def ev_row(self, ctx):
        await ctx.send(content="Az év amikor felvettek ide", components=[year_select])

    @cog_ext.cog_slash(name="faction_row", guild_ids=[308599429122883586, 737284142462402560], options=None)
    async def ga_row(self, ctx):
        await ctx.send(content="A szín aminek tagja vagy", components=[faction_select])

    @cog_ext.cog_slash(name="szak_row", guild_ids=[308599429122883586, 737284142462402560], options=None)
    async def _ka_row(self, ctx):
        await ctx.send(content="Ebben a képzésben veszel részt", components=[szak_select])

    @cog_ext.cog_slash(name="gm_row", guild_ids=[308599429122883586, 737284142462402560], options=None)
    async def _gm_row(self, ctx):
        await ctx.send(content="Ilyen játékokkal játszol", components=[gm_select])

    @cog_ext.cog_slash(name="ping_row", guild_ids=[308599429122883586, 737284142462402560], options=None)
    async def _ping_row(self, ctx):
        await ctx.send(content="Ezekre a pingekre vagy kíváncsi", components=[ping_select])
    
    """@commands.command(hidden = True)
    async def check_roles(self, ctx):
        emberek = await ctx.guild.fetch_members().flatten()
        roles = await ctx.guild.fetch_roles()
        for ember in emberek:
            for y in ember.roles:
                if "Gárda: " in y.name:
                    for z in roles:
                        if str(z.name) == "Generic gárda":
                            await ember.add_roles(z)
                            await asyncio.sleep(0.1)

                if "Szak: " in y.name:
                    for z in roles:
                        if str(z.name) == "Generic szak":
                            await ember.add_roles(z)
                            await asyncio.sleep(0.1)
            
                if "Évfolyam: " in y.name:
                    for z in roles:
                        if str(z.name) == "Generic évfolyam":
                            await ember.add_roles(z)
                            await asyncio.sleep(0.1)

        await ctx.send("Done!")"""

def setup(client):
    client.add_cog(slash_command_support(client))
    print("role selector is being loaded")

def teardown(client):
    client.remove_cog(slash_command_support(client))
    print("role selector is being unloaded")
