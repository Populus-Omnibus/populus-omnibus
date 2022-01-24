import re
import os
from unicodedata import name
import discord
import feedparser
from discord.ext import commands, tasks
from datetime import datetime
from discord_slash import SlashContext, cog_ext

import sys

sys.path.append('/home/ubuntu/server')

from filehandler import *

def get_data():
    tmpdict = (readsettings(segment="newschannels"))
    return tmpdict

addch = [{
    "name":"channel",
    "description": "Az a textchannel, ahova a hírek mennek",
    "required": True,
    "type": 7
}]

rmch = [{
    "name":"channel",
    "description": "Az a textchannel, ahova a hírek mennek",
    "required": True,
    "type": 7
}]
class News:
    def __init__(self, title, date, url, descr):
        self.title = title
        self.date = date
        self.url = url
        self.descr = descr

    def __str__(self):
        return '''{{
  title: {}
  date: {}
  url: {}
  descr: {}
}}'''.format(self.title, self.date[:-9], self.url, self.descr)

    def __repr__(self):
        return str(self)

sources = {'vik': 'https://vik.bme.hu/rss/', 'kth': 'https://kth.bme.hu/rss/'}

class viknews_by_BoA(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('viknews is ready')
        self.loops.start()
        
    @tasks.loop(seconds=10)
    async def loops(self):
        #print("loop")
        global sources
        for source in sources:
            news_list = get_news(sources[source])
            for index, news in enumerate(get_unseen(news_list, source)):
                print(news)
                seen_news(news_list, source)
                embed = discord.Embed(
                    title = news_list[index].title,
                    url = news_list[index].url,
                    colour = discord.Colour.blue()
                    )
                embed.add_field(name='Leírás: ', value=news_list[index].descr, inline=True)
                embed.set_thumbnail(url= self.client.user.avatar_url)
                embed.set_footer(text=news_list[index].date[:-9])

                lib = get_data()

                for x in lib:
                    csanel = self.client.get_channel(int(x))    #787045110168813598(announcement) 739557734705397812(viknews)
                    await csanel.send(embed = embed)

    @commands.command(brief = 'Hírek lekérése a vik.bme.huról.')
    async def viknews(self, ctx):
        global sources
        news_list = get_news(sources['vik'])
        embed = discord.Embed(
            title = news_list[0].title,
            url = news_list[0].url,
            colour = discord.Colour.blue()
            )
        embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
        embed.set_thumbnail(url= self.client.user.avatar_url)
        embed.set_footer(text=news_list[0].date[:-9])
        await ctx.channel.send(embed=embed)

    @commands.command(brief = 'Hírek lekérése a kth.bme.huról.')
    async def kthnews(self, ctx):
        global sources
        news_list = get_news(sources['kth'])
        embed = discord.Embed(
            title = news_list[0].title,
            url = news_list[0].url,
            colour = discord.Colour.blue()
            )
        embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
        embed.set_thumbnail(url= self.client.user.avatar_url)
        embed.set_footer(text=news_list[0].date[:-9])
        await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="add_news_channel", description="Beállítja a channelt, amibe az új hírek fognak menni.", guild_ids=[], options=addch)
    async def set_news_channel(self, ctx: SlashContext, channel):
        await ctx.defer(hidden=True)

        if channel.type == discord.ChannelType.text or channel.type == discord.ChannelType.news:
            print("based")
        else:
            await ctx.send(content="Ez nem egy text channel :woman_shrugging:", hidden=True)
            return

        lib = get_data()
        lib.append(channel.id)
        updatesettings(segment = "newschannels", data = lib)
        await ctx.send(content=f"Saved newschannel: {channel.name}  with ID: `{channel.id}`", hidden=True)

    @cog_ext.cog_slash(name="get_news_channel", description="Mutatja az összes newschannelt", default_permission=False, options=None, guild_ids=[])
    async def _get_news_channels(self, ctx: SlashContext):
        ctx.defer(hidden=True)

        lib = get_data()

        embed = discord.Embed(
            title = "News-channels",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url= self.client.user.avatar_url)
        for x in lib:
            ch = self.client.get_channel(int(x))
            embed.add_field(name=ch.name, value=f"Guild: {ch.guild}\nCategory: {ch.category}\nPosition: {ch.position}")

        await ctx.send(embed = embed, hidden=True)

    @cog_ext.cog_slash(name="remove_news_channel", description="Beállítja a channelt, amibe az új hírek fognak menni.", guild_ids=[], options=rmch)
    async def remove_news_channel(self, ctx: SlashContext, channel):
        await ctx.defer(hidden=True)

        if channel.type == discord.ChannelType.text or channel.type == discord.ChannelType.news:
            print("based")
        else:
            await ctx.send(content="Ez nem egy text channel :woman_shrugging:", hidden=True)
            return

        lib = get_data()

        if channel.id not in lib:
            await ctx.send(content="Nincs ilyen channel elmentve :woman_shrugging:")
            return

        lib.remove(channel.id)
        updatesettings(segment="newschannels", data = lib)
        await ctx.send(content=f"Törölve: {channel.name}  with ID: `{channel.id}`", hidden=True)

def setup(client):
    client.add_cog(viknews_by_BoA(client))
    print("viknews is being loaded")

def teardown(client):
    client.remove_cog(viknews_by_BoA(client))
    print("viknews is being unloaded")

def get_news(url):
    clean = re.compile('<.*?>')
    news = []
    feed = feedparser.parse(url)
    for news_item in feed['entries']:
        news.append(News(news_item.title, news_item.published, news_item.link, re.sub(clean, '', news_item.summary)))
    return news

def seen_news(news_list, source):
    seen_file = open('viknews/seen_'+source+'.txt', 'w')
    for news in news_list:
        seen_file.write(news.date+'\n')
    seen_file.close()

def get_unseen(news_list, source):
    unseen = []
    if not os.path.isfile('viknews/seen_'+source+'.txt'):
        return unseen
    seen_file = open('viknews/seen_'+source+'.txt')
    seen = [line.strip() for line in seen_file.readlines()]
    for news in news_list:
        if news.date not in seen:
            unseen.append(news)
    seen_file.close()
    return unseen
