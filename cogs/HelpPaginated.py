import aiohttp
import asyncio
import math
import aiohttp
import discord
import pymongo
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import checks
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

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

def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklisted.find_one({'user_id': author_id}):
            return False
        return True

    return commands.check(predicate)


async def get_prefix(bot, message):
    if message.guild:
        try:
            prefix = db.find_one({"guild_id": message.guild.id})["prefix"]
            return commands.when_mentioned_or(prefix)(bot, message)
        except(KeyError, AttributeError, TypeError):
            return commands.when_mentioned_or(prefix)(bot, message)



#Get all embeds into a list #Just append all embed names in here, in the right order ofcourse

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")



#Main command
    @commands.command(
        name = "help",
        aliases=["h"],
    )
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def help(self, ctx):
        prefix = db.find_one({"guild_id": ctx.guild.id})["prefix"]
        embed1 = discord.Embed(title=f'Help Center',
                                description=f'In this menu you can find out what commands we have and what they do\nTo get help on a certan command run `{prefix}help [command]`\nTo navigate the menu use ⬅️ and ➡️', inline=False,
                                color=0xE2BAB1)
        embed1.add_field(name=f'How do I add Asylum?',
                                value=f'Inviting Asylum is easy and free!\nTo invite me to your server click [here](https://discord.com/api/oauth2/authorize?client_id=871966033005645895&permissions=8&scope=bot)', inline=False)
        embed1.add_field(name=f'News Alerts',
                                value=f'New name and Pfp\nSlash Cmds coming soon smh', inline=True)
        embed2 = discord.Embed(title=f'Informational Commands',
                                description=f'{prefix}color - Shows said roles color\n{prefix}botinfo - Shows bot statistic\n{prefix}afk - sets you as afk\n{prefix}userinfo - Shows said users information\n{prefix}serverinfo - Shows said guilds information\n{prefix}ping - Shows the bots latency\n{prefix}permissions - Shows the users permissions\n{prefix}serveremotes - Shows the servers emotes\n{prefix}inrole - Shows every user with said role\n{prefix}discrim - Shows every user with said discriminator\n{prefix}avatar - Shows said users avatar\n{prefix}serveravatar - Shows the guilds icon\n{prefix}roleid - Shows the roles id\n{prefix}userid - Shows the users id\n{prefix}serverid - Shows the servers id\n{prefix}channelid - Shows the channels id', inline=False,
                                color=0xE2BAB1)
        embed3 = discord.Embed(title=f'Configuration Commands',
                                description=f'{prefix}welcome message - Sets the welcome message\n{prefix}welcome channel - Sets the welcome channel\n{prefix}welcome enable - Enables the welcome module\n{prefix}welcome disable - Disables the welcome module\n{prefix}welcome variables - Shows the configurable welcome variables\n{prefix}welcome config - Shows the welcome module config\n{prefix}autorole add - Adds a auto role on join\n{prefix}autorole remove - Removes a auto role on join\n{prefix}autorole config - Shows the auto-role module config\n{prefix}autorole enable - Enables the autrole module\n{prefix}autorole disable - Disables the autorole module\n{prefix}prefix - Sets the servers prefix\n{prefix}logchannel - Sets the servers log channel', inline=False,
                                color=0xE2BAB1)
        embed4 = discord.Embed(title=f'**Coming Soon!** - LastFM Cmds',
                                description=f'{prefix}set - Sets your LastFM username\n{prefix}unset - Unsets your LASTFM username\n{prefix}nowplaying - Shows what your currently playingn\n{prefix}topartists - Shows your top artists\n{prefix}toptags - Shows your top tags\n{prefix}profile - Sends your LastFM profile', inline=False,
                        color=0xE2BAB1)
        embed5 = discord.Embed(title=f'Fun Cmds',
                                description=f'{prefix}cuddle - Cuddle said user\n{prefix}hug - Hug said user <3\n{prefix}tickle - Tickle said user\n{prefix}kiss - Kiss said user <3 <3\n{prefix}pat - Pat said user\n{prefix}slap - Slap said user\n{prefix}fact - Sends a random fact\n{prefix}pin - Pins your message\n{prefix}unpin - Unpins your message\n{prefix}8ball - Determines the outcome of your question\n{prefix}tweet - creates a fake tweet\n{prefix}feed - Feed said user\n{prefix}spank - Spank said user\n{prefix}gif - Sends a random gif\n{prefix}searchgif - Searches for said gif\n{prefix}flip - Flips a coin\n{prefix}meme - Sends a random meme\n{prefix}lizard - Shows you a Lizard\n{prefix}bunny - Sends a picture of a Bunny\n{prefix}shiba - Shows you a Shiba', inline=False,
                        color=0xE2BAB1)
        embed6 = discord.Embed(title=f'Moderation Cmds',
                                description=f'{prefix}kick - Kicks said user\n{prefix}ban - Bans said user\n{prefix}unban - Unbans said user\n{prefix}hackban - Hackbans said user\n{prefix}purge - Purges said amount of messages\n{prefix}clear - Deletes said message content amount of times\n{prefix}clear embeds - Clears said amount of embed messages\n{prefix}clear files - Clears said amount of files\n{prefix}clear mentions - Clears said amount of mentions\n{prefix}clear images - Clears said amount of images\n{prefix}clear contains - Clears said amount of messages with a certain phrase\n{prefix}clear bots - Clears said amount of bot messages\n{prefix}clear emojis - Clears said amount of emoji messages\n{prefix}clear reactions - Removes said amount of reacions from messages\n{prefix}puser - Purges said amount of messages from a certain user\n{prefix}until - Clears all of the messages until said message id\n{prefix}role - Adds or Removes a role from said user\n{prefix}slowmode - Sets the channels slowmode\n{prefix}unslowmode - Removes a channels slowmode\n{prefix}nickname - Give said user said nickname', inline=False,
                        color=0xE2BAB1)
        embed7 = discord.Embed(title=f'Music Cmds',
                              description=f'{prefix}join - joins the voice channel\n{prefix}play - play a song youtube + spotify\n{prefix}stop - stops a the queue\n{prefix}queue - shows the queue\n{prefix}loop - loops the song\n{prefix}nowplaying - shows nowplaying\n{prefix}songsearch - searches songs on youtube\n{prefix}disconnect - leaves voice channel\n{prefix}skip - skips the song\n{prefix}move - moves to songs in the queue\n{prefix}clearqueue - clears the queue\n{prefix}pause - pauses the song\n{prefix}resume - resumes the song', inline=False,
                              color=0xE2BAB1)
        paginationList = [embed1, embed2, embed3, embed4, embed5, embed6, embed7]
        current = 0
        mainMessage = await ctx.send(
            embed = paginationList[current],
            components = [ #Use any button style you wish to :)
                [
                    Button(
                        label = "<",
                        id = "back",
                        style = ButtonStyle.grey
                    ),
                    Button(
                        label = ">",
                        id = "front",
                        style = ButtonStyle.grey
                    )
                ]
            ]
        )
        while True:
            try:
                interaction = await self.bot.wait_for(
                    "button_click",
                    check = lambda i: i.component.id in ["back", "front"],
                    timeout = 15.0
                )
                if interaction.component.id == "back":
                    current -= 1
                elif interaction.component.id == "front":
                    current += 1
                if current == len(paginationList):
                    current = 0
                elif current < 0:
                    current = len(paginationList) - 1

                await interaction.respond(
                    type = InteractionType.UpdateMessage,
                    embed = paginationList[current],
                    components = [
                        [
                            Button(
                                label = "<",
                                id = "back",
                                style = ButtonStyle.grey
                            ),
                            Button(
                                label = ">",
                                id = "front",
                                style = ButtonStyle.grey
                            )
                        ]
                    ]
                )
            except asyncio.TimeoutError:
                await mainMessage.edit(
                    components = [
                        [
                            Button(
                                label = "<",
                                id = "back",
                                style = ButtonStyle.grey,
                                disabled = True
                            ),
                            Button(
                                label = ">",
                                id = "front",
                                style = ButtonStyle.grey,
                                disabled = True
                            )
                        ]
                    ]
                )
                break

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def servers(self, ctx):
        """View all the servers i'm in"""
        page = 1
        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(self.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][0:20])
        s=discord.Embed(description=msg, colour=0x36393F, timestamp=__import__('datetime').datetime.utcnow())
        s.set_author(name="Servers ({})".format(len(self.bot.guilds)), icon_url=self.bot.user.avatar_url)
        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.bot.guilds))) / 20)))
        message = await ctx.send(embed=s)
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "▶" or reaction.emoji == "◀":
                        return True
        page2 = True
        while page2:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=reactioncheck)
                if reaction.emoji == "▶":
                    if page != math.ceil(len(list(set(self.bot.guilds))) / 20):
                        page += 1
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(self.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0x36393F, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(self.bot.guilds)), icon_url=self.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.bot.guilds))) / 20)))
                        await message.edit(embed=s)
                    else:
                        page = 1
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(self.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0x36393F, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(self.bot.guilds)), icon_url=self.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.bot.guilds))) / 20)))
                        await message.edit(embed=s)
                if reaction.emoji == "◀":
                    if page != 1:
                        page -= 1
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(self.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0x36393F, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(self.bot.guilds)), icon_url=self.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.bot.guilds))) / 20)))
                        await message.edit(embed=s)
                    else:
                        page = math.ceil(len(list(set(self.bot.guilds)))/ 20)
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(self.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=0x36393F, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(self.bot.guilds)), icon_url=self.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(self.bot.guilds))) / 20)))
                        await message.edit(embed=s)
            except asyncio.TimeoutError:
                try:
                    await message.remove_reaction("◀", ctx.me)
                    await message.remove_reaction("▶", ctx.me)
                except:
                    pass
                page2 = False

def setup(bot):
    bot.add_cog(Help(bot))