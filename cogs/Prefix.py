import discord
import pymongo
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

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

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")

    @commands.command(aliases=['set-prefix', 'pre', 'setprefix'])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    async def prefix(self, ctx, prefix: str):
        db.update_one({"guild_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
        embed = discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully updated the prefix to `{prefix}`\n", color=0x42EC8A)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Prefix(client))