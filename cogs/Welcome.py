import discord
import logging
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import pymongo
from utils.utils import utils

class welcome(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
mongoClient = pymongo.MongoClient(
    'mongodb+srv://Java:Merlin67@sirius.dmiob.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tls=True,
    tlsAllowInvalidCertificates=True)
db = mongoClient.get_database("Springs").get_collection("servers")
db2 = mongoClient.get_database("Springs").get_collection("protection")
db3 = mongoClient.get_database("Springs").get_collection("internal")
db4 = mongoClient.get_database("Springs").get_collection("punishments")
db5 = mongoClient.get_database("Springs").get_collection("antilimits")
db6 = mongoClient.get_database("Springs").get_collection("welcoming")
blacklisted = db3['blacklisted']




def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklisted.find_one({'user_id': author_id}):
            return False
        return True

    return commands.check(predicate)


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")

    @commands.group(invoke_without_command=True, name="welcome", description="Shows welcome commands", usage="welcome")
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def welcome(self, ctx):
        embed = discord.Embed(title="Help | Welcome", color=0xE2BAB1)
        embed.add_field(name="Commands", value="message\nchannel\nvariables\ndisable/enable\ntest", inline=False)
        await ctx.send(embed=embed)
 
    @welcome.command(name="message", description="Sets the welcome message", usage="welcome message <message>")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def message(self, ctx, *, message):
        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"message": message}})
        return await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully set the welcome message", color=0x42EC8A))

    @welcome.command(name="variables", description="Sets the welcome message", usage="welcome message <message>")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def variables(self, ctx):
        return await ctx.send(embed=discord.Embed(description="`{user.name}`\n`{user.mention}`\n`{user.tag}`\n`{user.id}`\n`{server.icon}`\n`{server.membercount}`\n`{server.name}`", color=0xE2BAB1))
 

    @welcome.command(name="channel", description="Sets the welcome channel", usage="welcome channel <channel>")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def channel(self, ctx, channel : discord.TextChannel):

        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"channel": channel.id}})
        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"channell": f'{channel.id}'}})
        return await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully set the welcome channel", color=0x42EC8A))

    @welcome.command(name="disable", description="Disables the welcome event", usage="welcome disable", aliases=["off"])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def disable(self, ctx):
        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome": "Disabled"}})
        return await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully disabled the welcome module", color=0x42EC8A))

    @welcome.command(name="enable", description="Enables the welcome event", usage="welcome enable")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def enable(self, ctx):
        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"welcome": "Enabled"}})
        return await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully enabled the welcome module", color=0x42EC8A))

    @welcome.command(name="config")
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def config(self, ctx):
        limit6 = db6.find_one({"guild_id": ctx.guild.id})['welcome']
        if limit6 == 'Disabled':
            pie = '<:Disabled:867864391550631936>'
        else:
            pie = '<:Enabled:867864464250372117>'
        channelk = db6.find_one({"guild_id": ctx.guild.id})['channell']
        embed = discord.Embed(title=f"Welcome Module", color=0xE2BAB1, description = f'<#{channelk}>\n')
        embed.add_field(name=f"Status", value=f"{pie}", inline=False)

    @welcome.command(name="test", description="Tests the welcome event", usage="welcome test")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def test(self, ctx):
        channel1 = db6.find_one({"guild_id": ctx.guild.id})['channel']
        message1 = db6.find_one({"guild_id": ctx.guild.id})['message']
        prefix = db.find_one({"guild_id": ctx.guild.id})["prefix"]

        if message1 == None:
            return await ctx.send(embed = discord.Embed(embed=discord.Embed(description=f"<:AsylumError:891452144476119101> No welcome message is selected, run the `{prefix}welcome message [message]` command", color=0xF38C28)))
        if channel1 == None:
            return await ctx.send(embed = discord.Embed(embed=discord.Embed(description=f"<:AsylumError:891452144476119101> No welcome message is selected, run the `{prefix}welcome channel [#channel]` command", color=0xF38C28)))

        channel = db6.find_one({"guild_id": ctx.guild.id})['channel']
        message = db6.find_one({"guild_id": ctx.guild.id})['message']
        user = ctx.author
        if "{user.id}" in message:
                message = message.replace("{user.id}", "%s" % (user.id))

        if "{user.mention}" in message:
            message = message.replace("{user.mention}", "%s" % (user.mention))

        if "{user.tag}" in message:
            message = message.replace("{user.tag}", "%s" % (user.discriminator))

        if "{user.name}" in message:
            message = message.replace("{user.name}", "%s" % (user.name))
            
        if "{user.avatar}" in message:
            message = message.replace("{user.avatar}", "%s" % (user.avatar_url))

        if "{server.name}" in message:
            message = message.replace("{server.name}", "%s" % (user.guild.name))
            
        if "{server.membercount}" in message:
            message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))
            
        if "{server.icon}" in message:
            message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

        try:

            channell = self.client.get_channel(channel)
            await channell.send(message)
            await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully tested the welcome message", color=0x42EC8A))
        except Exception:
            await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Unsuccessfully tested the welcome message", color=0xF38C28))

    @commands.Cog.listener()
    async def on_member_join(self, user):
        try:
            guild = user.guild
            channel1 = db6.find_one({"guild_id": guild.id})['channel']
            message1 = db6.find_one({"guild_id": guild.id})['message']


            if message1 == None:
                return
            if channel1== None:
                return

            channel = db6.find_one({"guild_id": guild.id})['channel']
            message = db6.find_one({"guild_id": guild.id})['message']
            if "{user.id}" in message:
                    message = message.replace("{user.id}", "%s" % (user.id))

            if "{user.mention}" in message:
                message = message.replace("{user.mention}", "%s" % (user.mention))

            if "{user.tag}" in message:
                message = message.replace("{user.tag}", "%s" % (user.discriminator))

            if "{user.name}" in message:
                message = message.replace("{user.name}", "%s" % (user.name))
                
            if "{user.avatar}" in message:
                message = message.replace("{user.avatar}", "%s" % (user.avatar_url))

            if "{server.name}" in message:
                message = message.replace("{server.name}", "%s" % (user.guild.name))
                
            if "{server.membercount}" in message:
                message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))
                
            if "{server.icon}" in message:
                message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

            await channel.send(message)
        except Exception:
            pass



def setup(client):
    client.add_cog(Welcome(client))