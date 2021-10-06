import os
import ssl
from pathlib import Path
import discord
import pymongo
from discord.ext import commands


intents = discord.Intents.all()
intents.members = True
cwd = Path(__file__).parents[0]
cwd = str(cwd)
ssl._create_default_https_context = ssl._create_unverified_context

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

async def get_prefix(bot, message):
    if message.guild:
        try:
            prefix = db.find_one({"guild_id": message.guild.id})["prefix"]
            return commands.when_mentioned_or(prefix)(bot, message)
        except(KeyError, AttributeError, TypeError):
            return commands.when_mentioned_or(prefix)(bot, message)

def NewServer(owner_id, server_id):
    db.insert_one({
        "whitelisted": [866723229635444786, owner_id],
        "prefix": '.',
        "log": None,
        "logg": "None",
        "muted": None,
        "jail": None,
        "jaill": "None",
        "captchalog": None,
        "captcalogg": "None",
        "minage": None,
        "temprole": None,
        "temproleafter": None,
        "premium": "No",
        "guild_id": server_id
    })
    db2.insert_one({
        "guild_id": server_id,
        "antinuke": 'Enabled',
        "antiraid": 'Disabled',
        "altidentifier": 'Disabled',
        "verification": 'Disabled',
        "antirole": 'Enabled',
        "antirole-del": 'Enabled',
        "antichannel": 'Enabled',
        "antichannel-del": 'Enabled',
        "antiban": 'Enabled',
        "antikick": 'Enabled',
        "antibot": 'Enabled',
    })
    db4.insert_one({
        "guild_id": server_id,
        "antiraidpun": "Ban",
        "altidentifierpun": 'Ban',
        "verificationpun": 'Ban',
        "antirolepun": 'Ban',
        "antirole-delpun": 'Ban',
        "antichannelpun": 'Ban',
        "antichannel-delpun": 'Ban',
        "antibanpun": 'Ban',
        "antikickpun": 'Ban',
        "antibotpun": 'Ban',
    })
    db5.insert_one({
        "guild_id": server_id,
        "antiraidlim": 10,
        "antirolelim": 1,
        "antirole-dellim": 1,
        "antichannellim": 1,
        "antichannel-dellim": 1,
        "antibanlim": 1,
        "antikicklim": 1,
        "antibotlim": 1,
    })
    db6.insert_one({
        "guild_id": server_id,
        "message": None,
        "channel": None,
        "channell": 'None',
        "color": None,
        "autoroles": [],
        "autrole": 'Disabled',
        "welcome": 'Disabled',


    })
    pass



token = '' #real token
#token = '' #dev token



client = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all(),
                                 help_command=None,
                                 owner_ids={843641951005442058, 852285257088892928, 815203787253350436, 791398221230243890})

@client.event
async def on_ready():
    for server in client.guilds:
        if not db.find_one({ "guild_id": server.id }):
            guild_ = client.get_guild(server.id)
            NewServer(guild_.owner.id, guild_.id)
            print(f'[\x1b[38;5;213mLOG\x1b[38;5;15m] Created DB For [\x1b[38;5;213m{server.name}\x1b[38;5;15m]')
    print(f'[\x1b[38;5;213mLOG\x1b[38;5;15m] Connected To [\x1b[38;5;213m{client.user}\x1b[38;5;15m]\n ---------------------------------')
    watch = discord.Activity(type = discord.ActivityType.watching, name=f'discord.gg/security')
    await client.change_presence(status=discord.Status.dnd, activity=watch)

@client.event
async def on_guild_join(guild):
    server = client.get_guild(guild.id)
    NewServer(server.owner.id, server.id)
    print(f'[\x1b[38;5;213mLOG\x1b[38;5;15m] Created DB For [\x1b[38;5;213m{server.name}\x1b[38;5;15m]')

@client.event
async def on_command_error(ctx, error: commands.CommandError):
  embed1 = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You are missing the needed `Permissions` to perform this command\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28)
  embed2 = discord.Embed(description=f"<:AsylumWrong:891703754703900702> You are missing the needed `Arguments` to perform this command\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28)
  embed3 = discord.Embed(description=f"<:AsylumWrong:891703754703900702>The selected `Member` could not be found\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28)
  embed4 = discord.Embed(description=f"<:AsylumWrong:891703754703900702> I am missing the needed `Permissions` to perform this command\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28)
  embed5 = discord.Embed(description=f"<:AsylumWrong:891703754703900702> This command is on a cooldown, please try again in {round(error.retry_after, 1)} seconds.\n<:AsylumSupport:891451343825412216> For support please join [here](https://discord.gg/n2fYsR2KMb)", color=0xF38C28)
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(embed=embed1)
  elif isinstance(error, commands.MissingRequiredArgument):
     await ctx.send(embed=embed2)
  elif isinstance(error, commands.MemberNotFound):
    await ctx.send(embed=embed3)
  elif isinstance(error, commands.BotMissingPermissions):
    await ctx.send(embed=embed4)
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send(embed=embed5)
  else:
    raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('_'):
        client.load_extension(f'cogs.{filename[:-3]}')


if __name__ == "__main__":
    client.run(token, reconnect=True)