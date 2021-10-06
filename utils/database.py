import datetime
import json
import os
import re
import discord
import pymongo
# Third party libraries
import asyncio
import os
from utils import utils
import asyncio
import time
import discord 
import pymongo
import os
import asyncio
import requests
from time import strftime
from discord.utils import find
from discord.ext import commands, tasks
import asyncio
from utils import utils
import time
import discord
from discord.ext import commands
from time import time
import time
from psutil import virtual_memory
import psutil
import discord
import asyncio
from discord.ext import commands
import time
import psutil

from colorama import Fore, Back, Style
import os
import discord
import pymongo
from discord.ext import commands

from utils import utils

import requests
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument

# Third party libraries
class database:

    mongoClient = pymongo.MongoClient('mongodb+srv://Java:Merlin67@sirius.dmiob.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tls=True, tlsAllowInvalidCertificates=True)
    db = mongoClient.get_database("Springs").get_collection("servers")
    db2 = mongoClient.get_database("Springs").get_collection("protection")