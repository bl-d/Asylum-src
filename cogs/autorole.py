import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import has_permissions
from utils.utils import utils
import pymongo

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

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[\x1b[38;5;213mLOG\x1b[38;5;15m] Cog Loaded: [\x1b[38;5;213m{self.__class__.__name__}\x1b[38;5;15m]")

    @commands.group(invoke_without_command=True, name="autorole", description="Shows welcome commands", usage="welcome")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def autorole(self, ctx):
        embed = discord.Embed(title="Help | Autorole", color=0xE2BAB1)
        embed.add_field(name="Commands", value="enable\nadd\nremove\ndisable\nconfig", inline=False)
        await ctx.send(embed=embed)

    @autorole.command(name="add")
    @commands.has_permissions(manage_roles=True)
    async def add(self, ctx, role: discord.Role):
        db6.update_one({"guild_id": ctx.guild.id}, {"$push": {"autoroles": role.id}})
        embed = discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully added {role.mention} to the auto-role list", color=0x42EC8A)
        await ctx.send(embed=embed)

    @autorole.command(name="remove")
    @has_permissions(manage_roles=True)
    async def remove(self, ctx, role: discord.Role):
            lmao = db6.find_one({"autoroles": role.id})
            if role.id not in lmao:
                embed1 = discord.Embed(description=f"<:AsylumError:891452144476119101> {role.mention} is not a selected auto-role", color=0xF38C28)
                return await ctx.send(embed=embed1)
            utils.pull_data(ctx.guild, "autoroles", role.id)
            embed= discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully removed {role.mention} from the auto-role list", color=0x42EC8A)

            await ctx.send(embed=embed)

    @autorole.command(name="disable")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disable(self, ctx):
        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"autrole": "Disabled"}})
        return await ctx.send(embed=discord.Embed(description="<:AsylumCorrect:891704856660832266> Successfully disabled the auto-role module", color=0x42EC8A))

    @autorole.command(name="enable")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enable(self, ctx):
        db6.update_one({"guild_id": ctx.guild.id}, {"$set": {"autrole": "Enabled"}})
        return await ctx.send(embed = discord.Embed(description=f"<:AsylumCorrect:891704856660832266> Successfully enabled the auto-role module", color=0x42EC8A))
        

    @autorole.command(name="config")
    @commands.cooldown(3, 14, BucketType.user)
    @blacklist_check()
    @commands.has_permissions(manage_roles=True)
    async def config(self, ctx):
        limit6 = db6.find_one({"guild_id": ctx.guild.id})['autrole']
        data = utils.find_data(ctx.guild)
        if limit6 == 'Disabled':
            pie = '<:Disabled:867864391550631936>'
        else:
            pie = '<:Enabled:867864464250372117>'
        for roleID in data['autoroles']:
            role = ctx.guild.get_role(roleID)
        embed = discord.Embed(title=f"Auto-Role On Join", color=0xE2BAB1, description = f'{role.mention}\n')
        embed.add_field(name=f"Status", value=f"{pie}", inline=False)


        
        await ctx.send(embed=embed)


    @commands.Cog.listener("on_member_join")
    async def autorole_event(self, member):
        data = utils.find_data(member.guild, "autoroles")
        for roleID in data:
            role = member.guild.get_role(roleID)
            await member.add_roles(role, reason="Asylum Auto-Role")

def setup(bot):
    bot.add_cog(Utility(bot))