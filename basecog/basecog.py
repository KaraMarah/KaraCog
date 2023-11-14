import discord
import string
import asyncio
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
        ctx = await self.bot.get_context(message)
        is_self = ctx.author == ctx.bot.user
        if not is_self:
            if ctx.author == 830225163722293258:
                ctx.send("this message is from mark!")