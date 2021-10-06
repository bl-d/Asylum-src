import datetime
from typing import Optional
from uuid import UUID

import asyncio
import discord
import re


def embed_create(ctx, title=discord.Embed.Empty, description=discord.Embed.Empty, color=0x46ff2e):
    embed = discord.Embed(description=description, title=title, color=color)
    embed.set_footer(
        text="Command sent by {}".format(ctx.author),
        icon_url=ctx.author.avatar_url,
    )
    return embed


def get_perms(permissions):
    perms = []
    if permissions.administrator:
        perms.append("Administrator")
    if permissions.manage_guild:
        perms.append("Manage guild")
    if permissions.ban_members:
        perms.append("Ban members")
    if permissions.kick_members:
        perms.append("Kick members")
    if permissions.manage_channels:
        perms.append("Manage channels")
    if permissions.manage_emojis:
        perms.append("Manage custom emotes")
    if permissions.manage_messages:
        perms.append("Manage messages")
    if permissions.manage_permissions:
        perms.append("Manage permissions")
    if permissions.manage_roles:
        perms.append("Manage roles")
    if permissions.mention_everyone:
        perms.append("Mention everyone")
    if permissions.manage_emojis:
        perms.append("Manage emojis")
    if permissions.manage_webhooks:
        perms.append("Manage webhooks")
    if permissions.move_members:
        perms.append("Move members")
    if permissions.mute_members:
        perms.append("Mute members")
    if permissions.deafen_members:
        perms.append("Deafen members")
    if permissions.priority_speaker:
        perms.append("Priority speaker")
    if permissions.view_audit_log:
        perms.append("See audit log")
    if permissions.create_instant_invite:
        perms.append("Create instant invites")
    if len(perms) == 0:
        perms.append("No moderator permissions")
    return perms


async def load_prefixes(bot):
    bot.prefixes = {}
    async with asqlite.connect('data.db', check_same_thread=False) as conn:
        async with conn.cursor() as cursor:
            for row in await cursor.execute("SELECT guild, prefix FROM prefixes"):
                bot.prefixes[row[0]] = row[1]
            await asyncio.sleep(5)
            await cursor.close()
        await conn.close()


class Emotes:
    botTag = "<:botTag:230105988211015680>"
    discord = "<:discord:314003252830011395>"
    owner = "<:owner:585789630800986114>"
    slowmode = "<:slowmode:585790802979061760>"
    check = "<:check:314349398811475968>"
    xmark = "<:xmark:314349398824058880>"
    role = "<:role:808826577785716756>"
    text = "<:channel:585783907841212418>"
    nsfw = "<:channel_nsfw:585783907660857354>"
    voice = "<:voice:585783907673440266>"
    emoji = "<:emoji_ghost:658538492321595393>"
    store = "<:store_tag:658538492409806849>"
    invite = "<:invite:658538493949116428>"

    # Badges
    partner = "<:partner:314068430556758017>"
    hypesquad = "<:hypesquad:314068430854684672>"
    nitro = "<:nitro:314068430611415041>"
    staff = "<:staff:314068430787706880>"
    balance = "<:balance:585763004574859273>"
    bravery = "<:bravery:585763004218343426>"
    brilliance = "<:brilliance:585763004495298575>"
    bughunter = "<:bughunter:585765206769139723>"
    supporter = "<:supporter:585763690868113455>"

    # Boost levels
    level1 = "<:booster:585764032162562058>"
    level2 = "<:booster2:585764446253744128>"
    level3 = "<:booster3:585764446220189716>"
    level4 = "<:booster4:585764446178246657>"

    verified = "<:verified:585790522677919749>"
    partnered = "<:partnernew:754032603081998336>"
    members = "<:members:658538493470965787>"
    stage = "<:stagechannel:824240882793447444>"
    stafftools = "<:stafftools:314348604095594498>"
    thread = "<:threadchannel:824240882697633812>"
    mention = "<:mention:658538492019867683>"
    rules = "<:rules:781581022059692043>"
    news = "<:news:658522693058166804>"

    @staticmethod
    def channel(chann):
        if chann.type == discord.ChannelType.text:
            if isinstance(chann, discord.TextChannel):
                if chann.is_nsfw():
                    return Emotes.nsfw
            return Emotes.text
        if chann.type == discord.ChannelType.news:
            return Emotes.news
        if chann.type == discord.ChannelType.voice:
            return Emotes.voice
        if chann.type == discord.ChannelType.store:
            return Emotes.store
        if chann.type == discord.ChannelType.category:
            return ""
        if chann.type == discord.ChannelType.private:
            return Emotes.thread
        if chann.type == discord.ChannelType.stage_voice:
            return Emotes.stage

    @staticmethod
    async def badges(user, bot):
        badge = " "
        u = await bot.fetch_user(user.id)
        flags = [name for name, value in dict.fromkeys(iter(u.public_flags)) if value]

        if user.bot:
            badge += Emotes.botTag
        if "staff" in flags:
            badge += Emotes.staff
        if "partner" in flags:
            badge += Emotes.partner
        if "hypesquad" in flags:
            badge += Emotes.hypesquad
        if "bug_hunter" in flags:
            badge += Emotes.bughunter
        if "early_supporter" in flags:
            badge += Emotes.supporter
        if "hypesquad_briliance" in flags:
            badge += Emotes.brilliance
        if "hypesquad_bravery" in flags:
            badge += Emotes.bravery
        if "hypesquad_balance" in flags:
            badge += Emotes.balance
        if "hypesquad_brilliance" in flags:
            badge += Emotes.brilliance
        if "verified_bot" in flags:
            badge += Emotes.verified
        if "verified_bot_developer" in flags:
            badge += Emotes.verified

        if (isinstance(user, discord.Member) and user.guild.premium_subscriber_role in user.roles) or \
                user.is_avatar_animated():
            badge += Emotes.nitro

        print(badge)
        return badge

    @staticmethod
    def boost(int):
        if int == 0:
            return ""
        if int == 1:
            return Emotes.level1
        if int == 2:
            return Emotes.level2
        if int == 3:
            return Emotes.level3
        if int == 4:
            return Emotes.level4


def is_uuid4(string):
    try:
        uuid = UUID(string, version=4)
    except ValueError:
        return False
    return uuid.hex == string


def get_from_guilds(bot, getter, argument):
    result = None
    for guild in bot.guilds:
        result = getattr(guild, getter)(argument)
        if result:
            return result
    return result


id_regex = re.compile(r'([0-9]{15,20})$')


def user_friendly_dt(dt: datetime.datetime):
    def format_dt(dt: datetime.datetime, style: Optional[str] = None) -> str:
        if style is None: return f'<t:{int(dt.timestamp())}>'
        return f'<t:{int(dt.timestamp())}:{style}>'
    return format_dt(dt, style='f') + f' ({format_dt(dt, style="R")})'