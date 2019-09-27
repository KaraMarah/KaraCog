import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core.utils.chat_formatting import pagify
from redbot.core import Config
import lyricsgenius

class GeniusCogTest(commands.Cog):
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
    async def genius(self, ctx, *search: str):
        geniusToken = await self.bot.db.api_tokens.get_raw("genius", default={"access_token": None})
        if geniusToken["access_token"] is None:
            return await ctx.send("The Genius access token has not been set. Use {}geniusapi for help.").format(ctx.prefix)
        genius = lyricsgenius.Genius(geniusToken["access_token"])
        genius.skip_non_songs = True
        genius.remove_section_headers = False
        song = genius.search_song(search)
        if len(song.lyrics) >= 2000
            pagelyrics = redbot.core.utils.chat_formatting.pagify(song.lyrics, delims = ['\n'])
            await ctx.send(pagelyrics)
        else:
            await ctx.send(song.lyrics)
