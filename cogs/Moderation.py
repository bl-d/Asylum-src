import discord
import time
import pymongo
import os
from discord import User, errors
import re
import typing
import typing as t
from discord.ext.commands import has_permissions, MissingPermissions, has_role, has_any_role
import asyncio
from utils import permissions, default
from datetime import datetime

from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands

# Connect to mongodb database
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


UNHOIST_PATTERN = "".join(chr(i) for i in [*range(0x20, 0x30), *range(0x3A, 0x41), *range(0x5B, 0x61)])

class Moderation(commands.Cog, name='Moderation'):
    def __init__(self, client):
        self.client = client
 

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")

    # Commands            
    @commands.command(
        name='kick',
        description='Kick someone from the server',
        usage='`.kick [@user]`'
    )
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        if ctx.author == member:
            await ctx.reply(
                embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot kick yourself\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        elif ctx.author.top_role < member.top_role:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot kick a member above you\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        elif ctx.guild.owner == member:
            await ctx.reply(
                embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot kick the guild owner\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        else:
            if reason == None:
                try:
                    try:
                        await member.kick()
                        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully kicked {member.mention}", color=0x42EC8A))
                    except:
                        await member.kick()
                        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully kicked {member.mention}", color=0x42EC8A))
                except:
                    await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not kick {member.mention}\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
            else:
                try:

                    await member.kick(reason=reason)
                    await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully kicked {member.mention} for {reason}", color=0x42EC8A))
                except:
                    await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not kick {member.mention}\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
                
    @commands.command(
        name='ban',
        description='Kick someone from the server',
        usage='`.kick [@user]`'
    )
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        if ctx.author == member:
            await ctx.reply(
                embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot ban yourself\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        elif ctx.author.top_role < member.top_role:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot ban a member above you\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        elif ctx.guild.owner == member:
            await ctx.reply(
                embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot ban the guild owner\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        else:
            if reason == None:
                try:
                    try:
                        await member.ban()
                        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully banned {member.mention}", color=0x42EC8A))
                    except:
                        await member.ban()
                        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully banned {member.mention}", color=0x42EC8A))
                except:
                    await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not ban {member.mention}\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
            else:
                try:

                    await member.ban(reason=reason)
                    await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully banned {member.mention} for {reason}", color=0x42EC8A))
                except:
                    await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not ban {member.mention}\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
                
    @commands.cooldown(3, 5, BucketType.user)           
    @commands.has_guild_permissions(manage_channels=True)
    @commands.command(name='nchannel', aliases=["createchannel", "cc", "newchannel"])
    async def new_channel(self, ctx, channel_name='text channel'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        await guild.create_text_channel(channel_name)
        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully created {channel_name}", color=0x42EC8A))
        
    @commands.command(aliases=["cr", "rolecreate"], usage=".createrole <rolename> [#hex] [#position] [permissions]")
    @commands.has_permissions(administrator=True)
    async def createrole(self, ctx, name:str="new role", clr:discord.Colour=0, pos:int=1, perms:int=0):
        _perms = discord.Permissions()
        _perms.value = perms

        clr = clr or discord.Colour(0)
        role = await ctx.guild.create_role(name=name, colour=clr, permissions=_perms)
        pos = pos if pos > 1 else 1
        await role.edit(position=pos)

        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully created {name}.", color=0x42EC8A))
                
    @commands.command(
        name='unban',
        description='Unbans the specified user.',
        usage='`.unban [@user]`'
    )
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def unban(self, ctx, userid, reason=None):

        if ctx.author == userid:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You cannot unban yourself\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        else: 
            try:
               user = discord.Object(id=userid)
               await ctx.guild.unban(user)
               await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully unbanned {userid} for {reason}", color=0x42EC8A))
            except:
                await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not unban that user\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))

    @commands.check_any(has_permissions(manage_messages=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    @commands.command(
        name='purge',
        aliases=["pu"],
        usage=".purge <amount>",
        hidden=True,
    )
    async def purge(
        self, ctx,
        num_messages: int,
    ):
        """Clear <n> messages from current channel"""
        channel = ctx.message.channel
        await ctx.message.delete()
        await channel.purge(limit=num_messages, check=None, before=None)
        return True

    @commands.group(aliases=["c"])
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.guild)
    @commands.check_any(has_permissions(manage_messages=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def clear(self, ctx):
        """ Removes messages from the current server. """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None, message=True):
        if limit > 2000:
            em = discord.Embed(description=f"<:AsylumWrong:891703754703900702> Too many messages to search given ({limit}/2000)", color=0xF38C28, delete_after=3)
            return await ctx.send(embed=em)

        if not before:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.HTTPException as e:
            em = discord.Embed(description=f"<:AsylumWrong:891703754703900702> Try a smaller search?", color=0xF38C28)
            return await ctx.send(embed=em)

        deleted = len(deleted)
        if message is True:
            await ctx.message.delete()
            await ctx.send(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully removed {deleted} message{'' if deleted == 1 else 's'}.", color=0x42EC8A, delete_after=3))

    @clear.command(aliases=["e"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds))

    @clear.command(aliases=["f"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""
        await self.do_removal(ctx, search, lambda e: len(e.attachments))

    @clear.command(aliases=["m"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def mentions(self, ctx, search=100):
        """Removes messages that have mentions in them."""
        await self.do_removal(ctx, search, lambda e: len(e.mentions) or len(e.role_mentions))

    @clear.command(aliases=["i"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @clear.command(name="all")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""
        await self.do_removal(ctx, search, lambda e: True)

    @clear.command(aliases=["co"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def contains(self, ctx, *, substr: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """
        if len(substr) < 3:
            await ctx.send("The substring length must be at least 3 characters.")
        else:
            await self.do_removal(ctx, 100, lambda e: substr in e.content)

    @clear.command(name="bots", aliases=["b"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def _bots(self, ctx, search=100, prefix=None):
        """Removes a bot user's messages and messages with their optional prefix."""

        getprefix = [";", "$", "!", "-", "?", ">", "^", "$", "w!", ".", ",", "a?", "g!", "m!", "s?"]

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or m.content.startswith(tuple(getprefix))

        await self.do_removal(ctx, search, predicate)

    @clear.command(name="emojis", aliases=["em"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def _emojis(self, ctx, search=100):
        """Removes all messages containing custom emoji."""
        custom_emoji = re.compile(r"<a?:(.*?):(\d{17,21})>|[\u263a-\U0001f645]")

        def predicate(m):
            return custom_emoji.search(m.content)

        await self.do_removal(ctx, search, predicate)
        
    @clear.command(name="reactions", aliases=["r"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        if search > 2000:
            return await ctx.send(f"Too many messages to search for ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully removed {total_reactions}.", color=0x42EC8A, delete_after=3))
    

    
    @commands.check_any(has_permissions(manage_messages=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    @commands.command(
        name='purge_user',
        hidden=True,
        aliases=['purgeu', 'purgeuser'],
    )
    async def puser(
        self, ctx,
        user: User,
        num_messages: typing.Optional[int] = 100,
    ):
        """Clear all messagges of <User> withing the last [n=100] messages"""
        channel = ctx.message.channel

        def check(msg):
            return msg.author.id == user.id

        await ctx.message.delete()
        await channel.purge(limit=num_messages, check=check, before=None)
    
    @commands.check_any(has_permissions(manage_messages=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    @commands.command(
        name='until',
        hidden=True,
        usage=".until <message-id>",
    )
    async def until(
        self, ctx,
        message_id: int,
    ):
        """Clear messages in a channel until the given message_id. Given ID is not deleted"""
        channel = ctx.message.channel
        try:
            message = await channel.fetch_message(message_id)
        except errors.NotFound:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> Could not find that message\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
            return

        await ctx.message.delete()
        await channel.purge(after=message)
        return True
    
 
     
            
    @commands.command(usage="@user/id <role_name>")
    @commands.check_any(has_permissions(manage_roles=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    @commands.cooldown(1, 2, commands.BucketType.user)
    @blacklist_check()
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        """Gives member a role.
        role: discord.Role
            The name of the role.
        member: discord.Member
            The member to give the role.
        """
        embed = discord.Embed(color=0x42EC8Ae)

        if (
            ctx.author != member
            and ctx.author.top_role <= member.top_role
            and ctx.guild.owner != ctx.author
        ):
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You can't change the role of someone higher than you\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))

        if (
            ctx.author == member
            and ctx.author.top_role <= role
            and ctx.guild.owner != ctx.author
        ):
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You can't give yourself a role higher than your highest role.\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))

        if role in member.roles:
            await member.remove_roles(role)
            embed = discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully removed {member.mention} from {role}", color=0x42EC8A)
            return await ctx.reply(embed=embed)

        await member.add_roles(role)
        embed = discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully added {role} to {member.mention}", color=0x42EC8A)
        return await ctx.reply(embed=embed)
            
            
    @commands.command(pass_context=True, usage="<seconds>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.check_any(has_permissions(manage_roles=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    async def slowmode(self, ctx, amount):
        await ctx.channel.edit(slowmode_delay=int(amount))
        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully slowed the channel.", color=0x42EC8A))
            
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.check_any(has_permissions(manage_roles=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+", "adm"))
    async def unslow(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully unslowed the channel.", color=0x42EC8A))
            
    @commands.command(aliases=['nick'], usage="@user/id <nickname>")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.check_any(has_permissions(manage_nicknames=True), has_any_role("mod", "moderator", "mods", "admin", "staff", "moderators", "+"))
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        """ Nicknames a user from the current server. """
        if await permissions.check_priv(ctx, member):
            return

        try:
            await member.edit(nick=name, reason=default.responsible(ctx.author, "Changed by command"))
            await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully changed {member.name} to {name}.", color=0x42EC8A))
        except:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not update that users nickname.\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
            

    
    @commands.command(
        name="hackban",
        description="Bans a user thats not in the server.",
        usage="`.hackban [id] [reason]`"
    )
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def hackban(self, ctx, userid, *, reason=None):

        try:
            userid = int(userid)
        except:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You gave a invalid ID, please give a valid ID\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
        
        try:
            await ctx.guild.ban(discord.Object(userid), reason=reason)
            await ctx.reply(embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully hackbanned {userid} for {reason}", color=0x42EC8A))
        except:
            await ctx.reply(embed = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I could not Hackban that ID\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28))
    

            
 
# Add cog
def setup(client):
    client.add_cog(Moderation(client))