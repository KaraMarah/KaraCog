from redbot.core import commands

class BaseCog(commands.Cog):
    """Custom commands for Isabelle Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def easypeasy(self, ctx):
        """This command does things"""
        await ctx.send("This is a command!")