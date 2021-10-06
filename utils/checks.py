from discord.ext import commands
import discord
import discord.utils
import json


def is_owner_check(ctx):
    if ctx.author.id in [815203787253350436]:
        return True
    else:
        return False


def is_main_owner():
    def predicate(ctx):
        if ctx.author.id in [815203787253350436]:
            return True

    return commands.check(predicate)


def is_owner():
    return commands.check(is_owner_check)


def is_owner_c(author):
    if author.id in [815203787253350436]:
        return True