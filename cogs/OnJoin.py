import aiohttp
import discord
import pymongo
from dhooks import Webhook, Embed
from discord.ext.commands.cooldowns import BucketType
from discord import Webhook, AsyncWebhookAdapter
import time
from discord.ext import commands



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
db4 = mongoClient.get_database("Springs").get_collection("punishments")
db5 = mongoClient.get_database("Springs").get_collection("antilimits")
db6 = mongoClient.get_database("Springs").get_collection("welcoming")
blacklisted = db3['blacklisted']

async def get_prefix(client, message):
    if message.guild:
        try:
            prefix = db.find_one({"guild_id": message.guild.id})["prefix"]
            return commands.when_mentioned_or(prefix)(client, message)
        except(KeyError, AttributeError, TypeError):
            return commands.when_mentioned_or(prefix)(client, message)

def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklisted.find_one({'user_id': author_id}):
            return False
        return True
    return commands.check(predicate)



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


class OnJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        embedelol = Embed(title="Secure Shard Ready",description=f'Shard #{shard_id} is ready', color=0x36393F)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("https://discord.com/api/webhooks/869690947980640316/7iiqH9FlYRyklBPNSMrqecOL1sCx--htDU0Itdo0m3VBSfk9SD_FW3gcsseaZHGBv-wo", adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=embedelol)

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        shardcn = Embed(title="Secure Connected",description=f'Secure has connected to shard #{shard_id}', color=0x36393F)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("https://discord.com/api/webhooks/869690947980640316/7iiqH9FlYRyklBPNSMrqecOL1sCx--htDU0Itdo0m3VBSfk9SD_FW3gcsseaZHGBv-wo", adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=shardcn)

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        shardcn = Embed(title="Secure Disconnected",description=f'Secure has disconnected to shard #{shard_id}', color=0x36393F)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("https://discord.com/api/webhooks/869690947980640316/7iiqH9FlYRyklBPNSMrqecOL1sCx--htDU0Itdo0m3VBSfk9SD_FW3gcsseaZHGBv-wo", adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=shardcn)

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id):
        shardcn = Embed(title=" Secure Resumed Connection",description=f'Secure has resumed connection to shard #{shard_id}', color=0x36393F)
        shardcn.set_thumbnail(url="https://i.imgur.com/tQbsvdB.png")
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("https://discord.com/api/webhooks/869690947980640316/7iiqH9FlYRyklBPNSMrqecOL1sCx--htDU0Itdo0m3VBSfk9SD_FW3gcsseaZHGBv-wo", adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=shardcn)



    @commands.Cog.listener()
    async def on_guild_join(self):
        for server in client.guilds:
            if not db.find_one({ "guild_id": server.id }):
                guild_ = client.get_guild(server.id)
                NewServer(guild_.owner.id, guild_.id)
                print(f'[\x1b[38;5;213mLOG\x1b[38;5;15m] Created DB For [\x1b[38;5;213m{server.name}\x1b[38;5;15m]')

    @commands.command(name="pingg")
    async def pingg(self, ctx: commands.Context):
        lol = (ctx.guild.shard_id + 1)
        loll = (round(self.bot.latencies[ctx.guild.shard_id][1]*1000))
        start_time = time.time()
        message = await ctx.send("Testing Asylums latency...")
        end_time = time.time()

        await message.edit(content=f"Shard: `{lol}`\nShard Latency: `{loll}ms`\nAPI: `{round((end_time - start_time) * 1000)}ms`")

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        server = client.get_guild(guild.id)
        db.delete_one({"guild_id": guild.id})
        db2.delete_one({"guild_id": guild.id})
        db4.delete_one({"guild_id": guild.id})
        db5.delete_one({"guild_id": guild.id})
        print(f'[\x1b[38;5;213mLOG\x1b[38;5;15m] Deleted DB For [\x1b[38;5;213m{server.name}\x1b[38;5;15m]')

def setup(client):
    client.add_cog(OnJoin(client))