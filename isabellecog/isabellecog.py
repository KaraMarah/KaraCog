import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify

class isabellecog(commands.Cog):
    """A set of custom commands for Isabelle Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def i(self, ctx, action: str, *, object: str):
        bad_words = ["fuck", "kill", "beat"]
        if action in bad_words:
            await ctx.send(f"I don't {action} {object} at all.")
        else:
            await ctx.send(f"I {action} {object} too, {ctx.author.mention}!")
