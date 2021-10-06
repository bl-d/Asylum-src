import datetime
import json
import os
import re
import discord
import pymongo
import requests
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument

# Third party libraries

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
bot_id = 842899285141225484


def create_embed(text):
    embed = discord.Embed(
        description=text,
        colour=0x36393F,
    )
    return embed


class utils:

    @classmethod
    def read_json(cls, path, data):
        """A simple json reading function."""
        with open(f"{path}.json", 'r') as f:
            result = json.load(f)

        return result[f"{data}"]

    @classmethod
    def format_logs(self):
        embed = discord.Embed(title="<:Bell:852619072692551751> Anti-Nuke Triggered", color=0x5865f2, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="<:News:852619060427358218> Reason:", value=f"`k`", inline=False)
 
        return embed

    @classmethod
    async def mute(self, guild: discord.Guild, member: discord.Member, reason=None):
        muted = discord.utils.get(guild.roles, name="Muted")
        if not muted:
            muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(muted, speak=False, send_messages=False, read_message_history=True, read_messages=True, connect=False)
        if reason == None:
            reason = f"{self.bot.user.name} | Mute"

        else:
            if muted in member.roles:
                return 
            else: 
                if len(member.roles) == 0:
                    pass
                else:
                    try:
                        for role in member.roles:
                            await member.remove_roles(role, reason=reason)
                    except:
                        pass
                
                await member.add_roles(muted, reason=reason)

    @classmethod
    def create_embed(cls, text):
        embed = discord.Embed(
            description=text,
            colour=0x5865f2,
        )
        return embed

    @classmethod
    def msg_contains_word(cls, msg, word):
        return re.search(fr'\b({word})\b', msg) is not None



    @classmethod
    def format_logs(self,):
        embed = discord.Embed(title="<:Bell:852619072692551751> Anti-Nuke Triggered", color=0x5865f2, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="<:Cpu:854516106127605821> User:", value="pp", inline=False)
        embed.add_field(name="<:News:852619060427358218> Reason:", value=f"hi", inline=False)
        embed.add_field(name="<:Banned:851939261729079357> Action Taken:", value=f"`k`", inline=False)
        return embed

    @classmethod
    def set_data(cls, typeKey: str, guild: discord.Guild, index: str, value):
        """Sets the data in a database."""
        db.update_one({"guild_id": guild.id}, {typeKey: {index: value}})

    @classmethod
    def find_data(cls, guild: discord.Guild, value: str = None):
        """Finds specific data in a database."""
        if value is not None:
            return db6.find_one({"guild_id": guild.id})[value]
        else:
            return db6.find_one({"guild_id": guild.id})

    @classmethod
    def contains(cls, object: discord.Role or discord.User or discord.TextChannel, guild: discord.Guild, value: str):
        if object.id in db.find_one({"guild_id": guild.id})[value]:
            return True
        else:
            return False

    @classmethod
    def set_toggle(cls, typeKey: str, guild: discord.Guild, index: str, value: bool):
        """Sets the toggle in a database."""
        db.update_one({"guild_id": guild.id}, {typeKey: {index: value}})

    @classmethod
    def upsert_data(cls, guild: discord.Guild, index: str, id):
        db.update_one({"guild_id": guild.id}, {"$push": {index: id}})

    @classmethod
    def pull_data(cls, guild: discord.Guild, index: str, id):
        db.update_one({"guild_id": guild.id}, {"$pull": {index: id}})

    @classmethod
    def delete_guild(cls, guild: discord.Guild):
        """Deletes the guild from selected database."""
        db.delete_one({"guild_id": guild.id})

    @classmethod
    def has_messagelogs(cls, guild: discord.Guild):
        if utils.find_data(guild, "message-logging") is True and utils.find_data(guild, "logging") is True:
            return True
        elif utils.find_data(guild, "log-channel") is None:
            return False
        else:
            return False

    @classmethod
    def has_modlogs(cls, guild: discord.Guild):
        if utils.find_data(guild, "mod-logging") is True and utils.find_data(guild, "logging") is True:
            return True
        elif utils.find_data(guild, "log-channel") is None:
            return False
        else:
            return False

    @classmethod
    def has_voicelogs(cls, guild: discord.Guild):
        if utils.find_data(guild, "voice-logging") is True and utils.find_data(guild, "logging") is True:
            return True
        elif utils.find_data(guild, "log-channel") is None:
            return False
        else:
            return False

    @classmethod
    def has_serverlogs(cls, guild: discord.Guild):
        if utils.find_data(guild, "server-logging") is True and utils.find_data(guild, "logging") is True:
            return True
        elif utils.find_data(guild, "log-channel") is None:
            return False
        else:
            return False

    @classmethod
    def has_userlogs(cls, guild: discord.Guild):
        try:
            if utils.find_data(guild, "user-logging") is True and utils.find_data(guild, "logging") is True:
                return True
            if utils.find_data(guild, "log-channel") is None:
                return False
            else:
                return False
        except:
            return False

    @classmethod
    def make_request(cls, type: str, url, headers=None, json=None):
        """Sends a get request."""
        if type == "GET" or "get":
            if headers is None or json is None:
                return requests.get(url)
            else:
                return requests.get(url, headers={'Authorization': f"Bot + {headers}"}, json=json)

        elif type == "POST" or "post":
            if headers is None or json is None:
                requests.post(url)
            else:
                requests.post(url, header={'Authorization': f"Bot + {headers}"}, json=json)

        elif type == "Put" or "put":
            if headers is None or json is None:
                requests.put(url)
            else:
                requests.put(url, header={'Authorization': f"Bot + {headers}"}, json=json)
        else:
            raise MissingRequiredArgument or AttributeError

    @classmethod
    def get_response(cls, type: str, url, headers=None, json=None):
        """Sends a get request with the response."""
        if type == "GET" or "get":
            if headers is None or json is None:
                return requests.get(url).json()
            else:
                return requests.get(url, headers={'Authorization': f"Bot + {headers}"}, json=json).json()
        else:
            raise MissingRequiredArgument or AttributeError

    @classmethod
    def setup(cls, bot: commands.AutoShardedBot):
        """Loads all bot cogs."""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') or '__pycache__' not in filename:
                bot.load_extension(f'cogs.{filename[:-3]}')
            else:
                print(f'Unable to load {filename[:-3]}')

    @classmethod
    def ffind_data(cls, guild: discord.Guild, value: str = None):
        """Finds specific data in a database."""
        if value is not None:
            return db.find_one({"guild_id": guild.id})[value]
        else:
            return db.find_one({"guild_id": guild.id})

    @classmethod
    async def get_prefix(cls, bot, message):
        """Gets the bot prefix."""
        if message.guild:
            try:
                prefix = db.find_one({"guild_id": message.guild.id})["prefix"]
                return commands.when_mentioned_or(prefix)(bot, message)
            except(KeyError, AttributeError, TypeError):
                return commands.when_mentioned_or(prefix)(bot, message)