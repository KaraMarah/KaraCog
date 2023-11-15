import discord
import string
import asyncio
import random
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify

class BaseCog(commands.Cog):
    """Custom commands for Isabelle Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def easypeasy(self, ctx):
        """This command does things"""
        await ctx.send("This is a command!")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Bait pings mark whenever he talks"""
        ctx = await self.bot.get_context(message)
        is_self = ctx.author == ctx.bot.user
        reactions = [":bait2:1167221593441829004", ":bait1:1167221594607865889"]
        if not is_self:
            if message.author.id == 830225163722293258:
                flip = random.randrange(2)
                await message.add_reaction(random.choice([":bait2:1167221593441829004", ":bait1:1167221594607865889"]))