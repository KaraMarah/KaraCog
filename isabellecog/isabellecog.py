import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify

class isabellecog(commands.Cog):
    """A set of custom commands for Isabelle Bot"""

    def __init__(self, bot):
        self.bot = Bot

    @commands.command()
    async def i(self, ctx, action: str, object: str):
        ctx.send("I " + action + object + " too, {}!").format(ctx.author)
