import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core import Config
import requests
import rauth

class GeniusCog(commands.Cog):
    """Fetches lyrics from Genius"""
    @commands.command()
    @checks.is_owner()
    async def geniusapi(self, ctx):
        """Set API info for Genius"""
        message = (
            "To get Genius API info:\n"
            "1. Create an API client at [Genius Developers](https://genius.com/developers)\n"
            "2. Copy your Client ID and Client secret.\n"
            "3. Use `{}set api genius clientid,<clientid_here> secret,<secret_here>`"
        ).format(ctx.prefix)
        await ctx.maybe_send_embed(message)

    # @commands.command()
    # @commands.guild_only()
    # async def genius(self, ctx, *, song: str):
    #     """Grabs the lyrics for a song from Genius"""
    #     apikeys = await self.bot.db.api_tokens.get_raw("genius", default={"clientid": none, "secret": none})
