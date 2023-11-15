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
            f"4. Use `{ctx.prefix}set api genius access_token,<token_here>`"
        )
        await ctx.maybe_send_embed(message)

    @commands.command()
    async def genius(self, ctx, *, search: str):
        """Grabs the lyrics from the requested song"""
        genius_token = await self.bot.get_shared_api_tokens("genius")
        if genius_token.get("access_token") is None:
            return await ctx.send(
                "The Genius access token has not been set. "
                f"Use `{ctx.prefix}geniusapi` for help."
            )
        else:
            song_search = lyricsgenius.Genius(genius_token["access_token"])
            song_search.verbose = False
            song_search.skip_non_songs = True
            song_search.remove_section_headers = False
            song = song_search.search_song(search)
            for page in pagify(song.lyrics):
                await ctx.send(page)
