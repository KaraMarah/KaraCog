import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify
from redbot.core import Config
import lyricsgenius

class GeniusCog(commands.Cog):
    """Fetches lyrics from Genius"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def geniusapi(self, ctx):
        """Set API info for Genius"""
        message = (
            "To get Genius API info:\n"
            "1. Create an API client at [Genius Developers](https://genius.com/developers)\n"
            "2. Generate a new access token.\n"
            "3. Copy your access token.\n"
            "4. Use `{}set api genius access_token,<token_here>`"
        ).format(ctx.prefix)
        await ctx.maybe_send_embed(message)

    @commands.command()
    async def genius(self, ctx, *, search: str):
        """Grabs the lyrics from the requested song"""
        geniusToken = await self.bot.get_shared_api_tokens("genius")
        if geniusToken.get("access_token") is None:
            return await ctx.send("The Genius access token has not been set. Use `{}geniusapi` for help.").format(ctx.prefix)
        else:
            songSearch = lyricsgenius.Genius(geniusToken["access_token"])
            songSearch.skip_non_songs = True
            songSearch.remove_section_headers = False
            song = songSearch.search_song(search)
            for page in pagify(song.lyrics):
                await ctx.send(page)
