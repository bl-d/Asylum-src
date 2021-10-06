import time
from psutil import Process, virtual_memory
import discord
import json
from discord import Embed, Color, Member, User, Status, Message, TextChannel, Role
from asyncio import sleep
from discord.ext.commands import Cog, command, cooldown, BucketType, group
import pymongo
import math
from discord.ext import commands
from typing import Union
import asyncio
from discord.ext.commands.cooldowns import BucketType
import re

import discord
import datetime
import time
import typing
import os
import codecs
import pathlib
import inspect

import itertools
import psutil
from io import BytesIO, StringIO
from PIL import Image

def solid_color_image(color: tuple):
    buffer = BytesIO()
    image = Image.new('RGB', (80, 80), color)
    image.save(buffer, 'png')
    buffer.seek(0)

    return buffer

def embed_create(ctx, title=discord.Embed.Empty, description=discord.Embed.Empty, color=0x46ff2e):
    embed = discord.Embed(description=description, title=title, color=color)
    return embed

def create_embed(text):
    embed = discord.Embed(
        description=text,
        colour=0x36393F,
    )
    return embed

mongoClient = pymongo.MongoClient(
    'mongodb+srv://Java:Merlin67@sirius.dmiob.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tls=True,
    tlsAllowInvalidCertificates=True)
db = mongoClient.get_database("Springs").get_collection("servers")
db2 = mongoClient.get_database("Springs").get_collection("protection")
db3 = mongoClient.get_database("Springs").get_collection("internal")
db4 = mongoClient.get_database("Springs").get_collection("punishments")
db5 = mongoClient.get_database("Springs").get_collection("antilimits")
blacklisted = db3['blacklisted']


def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklisted.find_one({'user_id': author_id}):
            return False
        return True

    return commands.check(predicate)

regex_mention = re.compile("<@(?:!|)(\d+)>")
regex_namediscrim = re.compile("(.{2,32})#(\d{4})")
regex_id = re.compile("(^\d+$)")
regex_name = re.compile("(.{2,32})")
role_mention = re.compile("<@&(\d+)>")
channel_mention = re.compile("<#(\d+)>")


def get_text_channel(ctx, channel):
    if channel_mention.match(channel):
        channel = discord.utils.get(ctx.guild.text_channels, id=int(channel_mention.match(channel).group(1)))
    elif regex_id.match(channel):
        channel = discord.utils.get(ctx.guild.text_channels, id=int(regex_id.match(channel).group(1)))
    else:
        try:
            channel = list(filter(lambda x: x.name.lower() == channel.lower(), ctx.guild.text_channels))[0]
        except IndexError:
            try:
                channel = list(filter(lambda x: x.name.lower().startswith(channel.lower()), ctx.guild.text_channels))[0]
            except IndexError:
                try:
                    channel = list(filter(lambda x: channel.lower() in x.name.lower(), ctx.guild.text_channels))[0]
                except IndexError:
                    return None
    return channel

def get_role(ctx, role):
    if role_mention.match(role):
        role = ctx.guild.get_role(int(role_mention.match(role).group(1)))
    elif regex_id.match(role):
        role = ctx.guild.get_role(int(regex_id.match(role).group(1)))
    else:
        try:
            role = list(filter(lambda x: x.name.lower() == role.lower(), ctx.guild.roles))[0]
        except IndexError:
            try:
                role = list(filter(lambda x: x.name.lower().startswith(role.lower()), ctx.guild.roles))[0]
            except IndexError:
                try:
                    role = list(filter(lambda x: role.lower() in x.name.lower(), ctx.guild.roles))[0]
                except IndexError:
                    return None
    return role

def get_bot_uptime(self, *, brief=False):
    now = datetime.datetime.utcnow()
    delta = now - self.bot.uptime
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if not brief:
        if days:
            fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h} hours, {m} minutes, and {s} seconds'
    else:
        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklisted.find_one({'user_id': author_id}):
            return False
        return True

    return commands.check(predicate)

async def entry_to_code(ctx, entries):
    width = max(map(lambda t: len(t[0]), entries))
    output = ['```']
    fmt = '{0:<{width}}: {1}'
    for name, entry in entries:
        output.append(fmt.format(name, entry, width=width))
    output.append('```')
    await ctx.send('\n'.join(output))

async def get_prefix(bot, message):
    if message.guild:
        try:
            prefix = db.find_one({"guild_id": message.guild.id})["prefix"]
            return commands.when_mentioned_or(prefix)(bot, message)
        except(KeyError, AttributeError, TypeError):
            return commands.when_mentioned_or(prefix)(bot, message)




class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")

    @staticmethod
    async def say_permissions(ctx, member, channel):
        permissions = channel.permissions_for(member)
        entries = [(attr.replace('_', ' ').title(), val) for attr, val in permissions]
        await entry_to_code(ctx, entries)



    @commands.command(name="permissions")
    @commands.guild_only()
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def _permissions(self, ctx, *, member: discord.Member = None):
        """Shows a member's permissions.
        You cannot use this in private messages. If no member is given then
        the info returned will be yours.
        """
        channel = ctx.message.channel
        if member is None:
            member = ctx.message.author

        await self.say_permissions(ctx, member, channel)





    @commands.command(aliases=["emotes", "emojis", "semotes", "semojis", "serveremojis"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def serveremotes(self, ctx):
        """View all the emotes in a server"""
        msg = ""
        for x in ctx.guild.emojis:
            if x.animated:
                msg += "<a:{}:{}> ".format(x.name, x.id)
            else:
                msg += "<:{}:{}> ".format(x.name, x.id)
        if msg == "":
            await ctx.send("There are no emojis in this server g")
            return
        else:
            i = 0 
            n = 2000
            for x in range(math.ceil(len(msg)/2000)):
                while msg[n-1:n] != " ":
                    n -= 1
                s=discord.Embed(description=msg[i:n], color=0xE2BAB1)
                i += n
                n += n
                if i <= 2000:
                    s.set_author(name="{} Emojis".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                await ctx.send(embed=s)

    @commands.command(aliases=['colour'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def color(self, ctx, *, color: Union[Color, Member, Role]):
        """Gets info for a color! You can specify a member, role, or color.
        Use the formats: `0x<hex>`, `#<hex>`, `0x#<hex>`, or `rgb(<num>, <num>, <num>)`"""
        alias = ctx.invoked_with.lower()

        color = color if isinstance(color, Color) else color.color

        buffer = await self.bot.loop.run_in_executor(None, solid_color_image, color.to_rgb())
        file = discord.File(filename="color.png", fp=buffer)

        embed = embed_create(ctx, title=f'Info for {alias}:', color=color)
        embed.add_field(name='Hex:', value=f'`{color}`')
        embed.add_field(name='Int:', value=f'`{str(color.value).zfill(8)}`')
        embed.add_field(name='RGB:', value=f'`{color.to_rgb()}`')
        embed.set_thumbnail(url="attachment://color.png")

        await ctx.send(file=file, embed=embed)
                
    @commands.command(usage="<reason>")
    async def afk(self, ctx, *, reason: str = 'None Provided'):
        with open('afks.json', 'r') as f:
            afks = json.load(f)

        try:
            if afks[str(ctx.author.id)]:
                afks.pop(str(ctx.author.id))
                with open('afks.json', 'w') as f:
                    json.dump(afks, f, indent=4)
                    embed = discord.Embed(description="<:AsylumError:891452144476119101> I have removed your AFK.", color=0xF38C28)
                return await ctx.reply(embed=embed)
        except KeyError:
            pass
        
        finaltime = str(ctx.message.created_at).split(
            ' ')[1].replace(':', '').replace('.', '')
        afks[str(ctx.author.id)] = {"message": reason, "time": finaltime}
        embed = discord.Embed(description="<:AsylumCorrect:891704856660832266> Your now marked as AFK.", color=0x42EC8A)
        await ctx.reply(embed=embed)
        await asyncio.sleep(1)
        with open('afks.json', 'w') as f:
            json.dump(afks, f, indent=4)

    @commands.Cog.listener(name="on_message")
    async def on_afk_say(self, message):

        if message.guild:
            with open('afks.json', 'r') as f:
                afks = json.load(f)

            try:
                if afks[str(message.author.id)]:
                    # replace the time with python struct, i forgot how it works sorry
                    longmess = int(int(str(message.created_at).split(" ")[1].replace(":", ".").replace(
                        ".", "")) - int(afks[str(message.author.id)]["time"])) / 1000000
                    _min, sec = divmod(longmess, 60)
                    hour, _min = divmod(_min, 60)
                    finalmess = "%d:%02d:%02d" % (hour, _min, sec)
                    embed = discord.Embed(description="<:AsylumError:891452144476119101> Your AFK has been removed.", color=0xF38C28)
                    await message.channel.send(embed=embed)
                    afks.pop(str(message.author.id))
                    with open('afks.json', 'w') as f:
                        json.dump(afks, f, indent=4)

            except KeyError:
                pass
            
    @commands.Cog.listener(name="on_message")
    async def on_afk_ping(self, message):

        if len(message.mentions):
            with open('afks.json', 'r') as f:
                afks = json.load(f)
            for i in message.mentions:
                if str(i.id) in afks and message.author != message.guild.me:
                    embed = discord.Embed(description=f'{i.display_name} is afk, reason: {afks[str(i.id)]["message"]}', color=0xF38C28)
                    await message.channel.send(embed=embed)
            
    @commands.command(pass_context=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def inrole(self, ctx, *, role: str):
        """Check who's in a specific role"""
        role = get_role(ctx, role)
        if not role:
            return await ctx.send("<:AsylumError:891452144476119101> Invalid role g")
        server = ctx.guild
        page = 1
        number = len(role.members)
        if number < 1:
            return await ctx.send("<:AsylumError:891452144476119101> There is no one in this role g")
        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
        s=discord.Embed(description=users, color=0xE2BAB1)
        s.set_author(name="Users who have the role " + role.name + " ({} users total)".format(number))
        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
        message = await ctx.send(embed=s)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "➡️" or reaction.emoji == "⬅️":
                        return True
        page2 = True
        while page2:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=reactioncheck)
                if reaction.emoji == "➡️":
                    if page != math.ceil(number / 20):
                        page += 1
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, color=0xE2BAB1)
                        s.set_author(name="Users who have the role  " + role.name + " ({} users total)".format(number))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
                    else:
                        page = 1
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, color=0xE2BAB1)
                        s.set_author(name="Users who have the role " + role.name + " ({} users total)".format(number))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
                if reaction.emoji == "⬅️":
                    if page != 1:
                        page -= 1
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, color=0xE2BAB1)
                        s.set_author(name="Users who have the role  " + role.name + " ({} users total)".format(number))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
                    else:
                        page = math.ceil(number / 20)
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, color=0xE2BAB1)
                        s.set_author(name="Users who have the role  " + role.name + " ({} users total)".format(number))
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
            except asyncio.TimeoutError:
                try:
                    await message.remove_reaction("⬅️", ctx.me)
                    await message.remove_reaction("➡️", ctx.me)
                except:
                    pass
                page2 = False

    @commands.command(pass_context=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def discrim(self, ctx, discriminator: str, page: int=None):
        """Check how many users have the discriminator 0001 seeing as though that's all people care about"""
        if not page:
            page = 1
        users = sorted([x for x in self.bot.users if x.discriminator == discriminator], key=lambda x: x.name)
        number = len(users)
        if page - 1 > number / 20:
            await ctx.send("<:AsylumError:891452144476119101> Invalid Page g")
            return
        if page < 1:
            await ctx.send("<:AsylumError:891452144476119101> Invalid Page g")
            return
        msg = "\n".join(list(map(lambda x: str(x), users))[page*20-20:page*20])
        if number == 0: 
            await ctx.send("<:AsylumError:891452144476119101> No one got this tag or its invalid g")
            return
        s=discord.Embed(title="{} users with the Discriminator #{}".format(number, discriminator), description=msg, color=0xE2BAB1)
        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
        await ctx.send(embed=s)

    @commands.command(pass_context=True, aliases=["uid"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def userid(self, ctx, *, user: discord.Member=None):
        """Get someone userid"""
        author = ctx.message.author
        if not user:
            user = author
        await ctx.send("`{}`'s ID: `{}`".format(user, user.id))
        
    @commands.command(pass_context=True, aliases=["rid"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def roleid(self, ctx, *, role: discord.Role):
        """Get a roles id"""
        await ctx.send("`{}`'s ID: `{}`".format(role.name, role.id))
    
    @commands.command(pass_context=True, aliases=["sid"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def serverid(self, ctx):
        """Get the servers id"""
        server = ctx.guild
        await ctx.send("{}'s ID: `{}`".format(server.name, server.id))
        
    @commands.command(pass_context=True, aliases=["cid"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def channelid(self, ctx, *, channel: str=None):
        """Get a channels id"""
        if not channel:
            channel = ctx.message.channel
        else:
            channel = get_text_channel(ctx, channel)
            if not channel:
                return await ctx.send("I could not find that channel g")
        await ctx.send("<#{}> ID: `{}`".format(channel.id, channel.id))

    @commands.command(pass_context=True, aliases=["av"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def avatar(self, ctx, *, user: discord.Member=None):
        """Look at your own or someone elses avatar"""
        author = ctx.message.author
        if not user:
            user = author
        s=discord.Embed(color=0xE2BAB1)
        s.set_author(name="{}'s Avatar".format(user.name), url=user.avatar_url)
        s.set_image(url=user.avatar_url_as(size=1024))
        await ctx.send(embed=s)
        
    @commands.command(aliases=["savatar"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def serveravatar(self, ctx):
        """Look at the current server avatar"""
        server = ctx.guild
        color=0xE2BAB1
        s=discord.Embed(colour=discord.Colour(value=color))
        s.set_author(name="{}'s Icon".format(server.name), url=server.icon_url_as(format="png", size=1024))
        s.set_image(url=server.icon_url_as(format="png", size=1024))
        await ctx.send(embed=s)

    @commands.command(name="serverinfo", description="Shows server information", usage="serverinfo", aliases=["sinfo"])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def serverinfo(self, ctx):
        guild = ctx.guild.created_at.strftime("%B %dth %Y, %I:%M %p")
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categorys = len(ctx.guild.categories)
        embed = discord.Embed(color=0xE2BAB1)
        embed.add_field(name=f"Name {(ctx.guild.name)}", value=f"ID: `{ctx.guild.id}`\nOwner: `{ctx.guild.owner}`\nCreated: `{guild}`", inline=False)
        online = 0
        offline = 0
        dnd = 0
        idle = 0
        bots = 0
        for member in ctx.guild.members:
            if member.status == discord.Status.online:
                online += 1
            if member.status == discord.Status.offline:
                offline += 1
            if member.status == discord.Status.dnd:
                dnd += 1
            if member.status == discord.Status.idle:
                idle += 1
            if member.bot:
                bots += 1
        embed.add_field(name="Members", value=f"Total Members: `{len(ctx.guild.members)}`\n Total Bots: `{bots}`\n Online: `{online}`\nOffline: `{offline}`\nIdle: `{idle}`\n Do Not Disturb: `{dnd}`", inline=False)
        embed.add_field(name="Misc", value=f"Total Categorys: `{categorys}`\n Total Channels: `{text_channels}`\n Total Voice Channels: `{voice_channels}`\n Total Roles: `{len(ctx.guild.roles)}`", inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)



    @commands.command(name="ping")
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def ping(self, ctx: commands.Context):
        lol = (ctx.guild.shard_id + 1)
        loll = (round(self.bot.latencies[ctx.guild.shard_id][1]*1000))
        start_time = time.time()
        message = await ctx.send("Testing Asylums latency...")
        end_time = time.time()

        await message.edit(content=f"Shard: `{lol}`\nShard Latency: `{loll}ms`\nAPI: `{round((end_time - start_time) * 1000)}ms`")

    @commands.command()
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if member == '':
            member = ctx.author
        whitelisted = db.find_one({"guild_id": ctx.guild.id})['whitelisted']
        if member.id in whitelisted:
            whitelistcheck = "Yes"
        else:
            whitelistcheck = "No"
        embed = discord.Embed(title='Userinfo', color=0xE2BAB1)
        embed.add_field(name="Name: {}".format(member.display_name), value="Tag: `{}#{}`\nID: `{}`".format(member.display_name, member.discriminator, member.id), inline=False)
        embed.add_field(name="Dates", value=f'Creation: {member.created_at.strftime("`%B %dth %Y, %I:%M %p`")}\nJoined: {member.joined_at.strftime("`%B %dth %Y, %I:%M %p`")}', inline=False)
        if member.status == discord.Status.online:
            statuss="Online"
        if member.status == discord.Status.idle:
            statuss="Idle"
        if member.status == discord.Status.do_not_disturb:
            statuss="Dnd"
        if member.status == discord.Status.offline:
            statuss="Offline"        
        embed.add_field(name="Misc", value=f"Colour: `{(member.colour)}`\nStatus: `{statuss}`\nRole Count: `{len(member.roles) - 1}`\nHighest Role: `{member.top_role}`", inline=False)
        blacklist = blacklisted.find()
        if member.id in blacklist:
            blacklistcheck = "Yes"
        else:
            blacklistcheck = "No"
        embed.add_field(name="Asylum Information", value=f"Strikes: `0`\nWhitelisted: `{whitelistcheck}`", inline=False)

        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)




    @commands.command(aliases=['bot-info', 'stats'])
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def botinfo(self, ctx):
        proc = Process()
        with proc.oneshot():
            commands = (len(self.bot.commands))
            total_members = sum(len(s.members) for s in ctx.bot.guilds)
            total_online = sum(1 for m in ctx.bot.get_all_members() if m.status != discord.Status.offline)
            unique_members = set(ctx.bot.get_all_members())
            unique_online = sum(1 for m in unique_members if m.status != discord.Status.offline)
            text = sum([len(guild.text_channels) for guild in ctx.bot.guilds])
            voice = sum([len(guild.voice_channels) for guild in ctx.bot.guilds])
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)
            mem_usage = mem_total * (mem_of_total / 100)
            channels = f'<:AsylumVersion:891451024420794378> Version: `0.1`\n<:AsylumStorage:891450424681459752> Total Storage: `{mem_usage:,.3f} MB`\n<:AsylumSupport:891451343825412216> Support Server: [here](https://discord.gg/n2fYsR2KMb)'
            members = f"<:AsylumGuilds:891449788057419846> Guilds: `{len(self.bot.guilds)}`\n<:AsylumUsers:891449330421071893> Users: `{total_members:,}`\n<:AsylumUsers:891449330421071893> Unique: `{len(unique_members):,}`"
        embed = discord.Embed(
            title=f'Asylum Info',color=0xE2BAB1
        )
        embed.add_field(name="System",
                        value=channels,
                        inline=True)
        embed.add_field(name="Statistics",
                        value=members,
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def invite(self, ctx):
        await ctx.send(f"https://discord.com/api/oauth2/authorize?client_id=871966033005645895&permissions=8&scope=bot")




    @commands.command()
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def logchannel(self, ctx, channel : discord.TextChannel):
        db.update_one({"guild_id": ctx.guild.id}, {"$set": {"log": channel.id}})
        db.update_one({"guild_id": ctx.guild.id}, {"$set": {"logg": f'{channel.id}'}})
        return await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully set the log channel", color=0xE2BAB1))

def setup(bot):
    bot.add_cog(Information(bot))