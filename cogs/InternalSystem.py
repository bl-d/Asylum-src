import aiohttp
import asyncio
import math
import aiohttp
import traceback
import os
import discord
import pymongo
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import checks

def create_embed(text):
    embed = discord.Embed(
        description=text,
        colour=0x36393F,
    )
    return embed

client = discord.Client()
mongoClient = pymongo.MongoClient(
    'mongodb+srv://Java:Merlin67@sirius.dmiob.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tls=True,
    tlsAllowInvalidCertificates=True)
db = mongoClient.get_database("Springs").get_collection("servers")
db2 = mongoClient.get_database("Springs").get_collection("protection")
db3 = mongoClient.get_database("Springs").get_collection("internal")
blacklisted = db3['blacklisted']

def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklisted.find_one({'user_id': author_id}):
            return False
        return True

    return commands.check(predicate)


async def get_prefix(client, message):
    if message.guild:
        try:
            prefix = db.find_one({"guild_id": message.guild.id})["prefix"]
            return commands.when_mentioned_or(prefix)(client, message)
        except(KeyError, AttributeError, TypeError):
            return commands.when_mentioned_or(prefix)(client, message)


class InternalSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")


    @commands.command(
        name='reload', description="Reload all/one of the bots cogs!"
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                message = await ctx.send("Reloading all cogs")
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.client.unload_extension(f"cogs.{ext[:-3]}")
                            self.client.load_extension(f"cogs.{ext[:-3]}")

                            message = await ctx.send(f"Reloaded: `{ext}`\n")
                        except Exception as e:

                            message = await ctx.send(f"Failed to reload: `{ext}`")

        else:
            # reload the specific cog
            async with ctx.typing():
                message = await ctx.send("Reloading all cogs")
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    message = await ctx.send(f"Failed to reload: `{ext}`\n This cog doesnt exist g")

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.client.unload_extension(f"cogs.{ext[:-3]}")
                        self.client.load_extension(f"cogs.{ext[:-3]}")
                        message = await ctx.send(f"Reloaded: `{ext}`\n")
                    except Exception:
                        desired_trace = traceback.format_exc()
                        message = await ctx.send(f"Failed to reload: `{ext}`\n{desired_trace}")
                await ctx.send(message)

    @commands.command(
        name='serverss',
        description='Owner Only | List the servers that the bot is in',
        usage='serverss',
        aliases=["serverlisst"]
    )
    @commands.is_owner()
    async def serverss(self, ctx, page: int = 1):
        output = ''
        guilds = self.client.guilds
        pages = math.ceil(len(guilds)/15)
        if 1 <= page <= pages:
            counter = 1+(page-1)*15
            for guild in guilds[(page-1)*15:page*15]:
                gn = guild.name
                gi = str(guild.id)
                gm = str(len(guild.members))
                go = str(guild.owner)
                output += f'**{counter}.** `{gn}` **|** `{gi}` **|** `{gm}` **|** `{go}`\n'
                counter += 1
            embed = discord.Embed(
                colour=self.colour,
                description=output,
                title='__**Server List**__',
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f'Page {page} of {pages}'
            )
            msg = await ctx.send(
                embed=embed
            )
            await msg.add_reaction("<a:L_Arrow:767064087367647242>")
            await msg.add_reaction("<a:R_Arrow:767064076512919552>")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["<a:R_Arrow:767064076512919552>", "<a:L_Arrow:767064087367647242>"]
            while True:
              try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "<a:L_Arrow:767064087367647242>":
                  page += 1
                elif str(reaction.emoji) == "<a:R_Arrow:767064076512919552>":
                  page -= 1
              except asyncio.TimeoutError:
                await msg.remove_reaction(reaction, ctx.author)
                await msg.remove_reaction(reaction, ctx.author)
                await msg.remove_reaction(reaction, self.client.user)
                await msg.remove_reaction(reaction, self.client.user)
        else:
            await ctx.send(
                embed=create_embed(
                    'Invalid Page Number.'
                ),
                delete_after=10
            )


    @commands.command(
        name='leaveserver',
        description='Owner Only | Leave the server of your choice',
        usage='leaveserver <number on list>'
    )
    @checks.is_owner()
    async def leaveserver(self, ctx, pos: int):
        guilds = self.client.guilds
        guild = guilds[pos - 1]
        await guild.leave()
        await ctx.send(
            embed=create_embed(
                f'Left {guild.name}'
            )
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for channel in guild.text_channels:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/863814492064448526"
                    "/N3Fes8OJscTuUewu0zxzjncur74kBrCotD4Iizy_j6kOYDCmaFNGIaKzvuz_zBuRVK6U")
            log = DiscordEmbed(title=f"Left A Server",
                               description=f"Name: **{guild.name}**\nOwner: **{guild.owner}**\nMembers: **{len(guild.members)}**\n **Botinfo**\n users: {len(set(self.client.get_all_members()))}\n servers: {len(self.client.guilds)}")
            webhook.add_embed(log)
            webhook.execute()
            break

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            link = await channel.create_invite(max_age=0, max_uses=0)
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/868947897025175662/wbJA80R0hJbX8MKzBp-tp_YFSGIGaPRonB94U7DtC_79"
                    "-toJXFSYR16YAat2Txde7AEL")
            log = DiscordEmbed(title=f"Joined A Server",
                               description=f"Name: **{guild.name}**\nOwner: **{guild.owner}**\nInvite: [**Join Here**]({link})\nMembers: **{len(guild.members)}**\n **Botinfo**\n users: {len(set(self.client.get_all_members()))}\n servers: {len(self.client.guilds)}")
            webhook.add_embed(log)
            webhook.execute()
            break

    @commands.Cog.listener()
    async def on_command_completion(self, ctx, **kwargs):
        guild = self.client.get_guild(863805312862257172)
        channel = guild.get_channel(865676729938346004)
        webhook = DiscordWebhook(
            url="https://discord.com/api/webhooks/869595809119887381/iFHFKkAochsAfvXybP5VZ8HnyGYtqEsKvrvj_DJ_tdGYgFMdB7KYEEIfeXPiqrOnJ1d7")
        s = discord.Embed(colour=0x36393F,
                          timestamp=ctx.message.edited_at if ctx.message.edited_at else ctx.message.created_at)
        s.add_field(name="Message", value="Content: `{}`\nID: `{}`".format(ctx.message.content, ctx.message.id),
                    inline=False)
        s.add_field(name="Channel", value="Name: `{}`\nID: `{}`".format(ctx.channel.name, ctx.channel.id), inline=False)
        s.add_field(name="Guild",
                    value="Name: `{}`\nID: `{}`\nMember Count: `{:,}`".format(ctx.guild.name, ctx.guild.id,
                                                                              ctx.guild.member_count), inline=False)
        s.add_field(name="Author", value="User: `{}`\nID: `{}`".format(ctx.author, ctx.author.id), inline=False)
        s.add_field(name="Command",
                    value="Prefix: `{}`\nCommand: `{}`\nArguments: `{}`".format(ctx.prefix, ctx.command, kwargs),
                    inline=False)
        s.add_field(name="Attachments", value="\n".join(
            map(lambda x: x.url, ctx.message.attachments)) if ctx.message.attachments else "None", inline=False)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                "https://discord.com/api/webhooks/869595809119887381/iFHFKkAochsAfvXybP5VZ8HnyGYtqEsKvrvj_DJ_tdGYgFMdB7KYEEIfeXPiqrOnJ1d7",
                adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=s)

    @commands.command(
        name='getserver',
        description='Owner Only | Gets info on the given server id.',
        usage='getserver <guild_id>',
        aliases=["getguild"]
    )
    @checks.is_owner()
    async def getserver(self, ctx, id: int):
        output = ''
        guild = self.client.get_guild(id)
        if not guild:
            return await ctx.send("Unkown Guild ID. This is likely caused by me not being in the specified guild id.")
        gn = guild.name
        gi = str(guild.id)
        gm = str(len(guild.members))
        go = str(guild.owner)
        output += f'Name: `{gn}`\nID: `{gi}`\nMembers: `{gm}`\nOwner: `{go}`\nInvite: `fetching...`'
        embed = discord.Embed(
            color=0x36393F,
            title=f'Guild Info For ID: {id}',
            description=output,
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)

    @commands.command(
        name='getuser',
        description='Owner Only | Gets info on the given user id.',
        usage='getuser <userid>'
    )
    @checks.is_owner()
    async def getuser(self, ctx, id: int):
        output = ''
        user = self.client.get_user(id)
        if not user:
            return await ctx.send(
                "Unkown User ID. This is likely caused by me not having any mutuals with the given user.")
        un = user.name
        ui = str(user.id)
        ug = ''
        ugc = 0
        guilds = self.client.guilds
        for guild in guilds:
            if guild.owner.id == id:
                ug += f"`{guild.name}`\n"
                ugc += 1
        if ug == '': ug = "**None.**"
        output += f'Name: `{un}`\nID: `{ui}`\nServers: ({ugc})\n{ug}'
        embed = discord.Embed(
            color=0x36393F,
            title=f'Private User Info For ID: {id}',
            description=output,
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)

    @commands.command(
        name='blacklist',
        description='Owner Only | Blacklist users from using the bot',
        usage='blacklist <userid>'
    )
    @checks.is_owner()
    async def blacklist(self, ctx, userid: int, *, reason=None):
        if blacklisted.find_one({'user_id': userid}):
            await ctx.send(
                embed=create_embed(
                    'User ID already blacklisted.'
                )
            )
        else:
            if self.client.get_user(userid) != None:
                blacklisted.insert_one({'user_id': userid})
                await ctx.send(
                    embed=create_embed(
                        f'User, <@{userid}> is now blacklisted.'
                    )
                )
                user = self.client.get_user(userid)
                await user.send(embed=create_embed(
                    f'**Alert**\nYou have been blacklisted from `Asylum`\nReason: `{reason}`\nIf you would like to appeal this Blacklist contact `Java#0009`'))
            else:
                await ctx.send(
                    embed=create_embed(
                        'Unknown User ID. Please make sure that user is in a server that I am in!'
                    ),
                    delete_after=30
                )

    @commands.command(
        name='showblacklist',
        description='Owner Only | List of all blacklisted users.',
        usage='showblacklist <page>'
    )
    @checks.is_owner()
    async def showblacklist(self, ctx, page: int = 1):
        output = ''
        blacklist = blacklisted.find()
        pages = math.ceil(blacklist.count() / 10)
        if 1 <= page <= pages:
            counter = 1 + (page - 1) * 10
            for user in blacklist[(page - 1) * 10:page * 10]:
                user = self.client.get_user(user['user_id'])
                output += f'**{counter}.** `{user.name}` | `{user.id}`\n'
                counter += 1
            embed = discord.Embed(
                color=0x36393F,
                title='**__Blacklisted Users__**',
                description=output,
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f'Page {page} of {pages}'
            )
            await ctx.send(
                embed=embed
            )
        else:
            await ctx.send(
                embed=create_embed(
                    'The specified page does not exist'
                ),
                delete_after=10
            )

    @commands.command(
        name='unblacklist',
        description='Owner Only | Remove\'s a user from the blacklist.',
        usage='unblacklist <userid>'
    )
    @checks.is_owner()
    async def unblacklist(self, ctx, userid: int):
        if blacklisted.find_one({'user_id': userid}):
            blacklisted.delete_one({'user_id': userid})
            await ctx.send(
                embed=create_embed(
                    f'User, <@{userid}> has been unblacklisted.'
                ),
                delete_after=30
            )
        else:
            await ctx.send(
                embed=create_embed(
                    f'User, <@{userid}> is not blacklisted.'
                ),
                delete_after=10
            )


def setup(client):
    client.add_cog(InternalSystem(client))
