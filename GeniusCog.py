import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.utils import chat_formatting as chat
from redbot.core import Config
import lyricsgenius

class GeniusCog(commands.Cog):
    """Fetches lyrics from Genius"""
    @commands.command()
    @checks.is_owner()
    async def geniusapi(self, ctx):
        """Set API info for Genius"""
        message = (
            "To get Genius API info:\n"
            "1. Create an API client at [Genius Developers](https://genius.com/developers)\n"
            "2. Generate a new access token.\n"
            "3. Copy your access token.\n"
            "3. Use `{}set api genius access_token,<token_here>`"
        ).format(ctx.prefix)
        await ctx.maybe_send_embed(message)

    @commands.command()
    async def genius(self, ctx, *title: str, *artist: str):
        geniusToken = await self.bot.db.api_tokens.get_raw("genius", default={"access_token": None})
        if geniusToken["access_token"] is None:
            return await ctx.send("The Genius access token has not been set.")
        genius = lyricsgenius.Genius(geniusToken["access_token"])
        genius.skip_non_songs = True
        genius.remove_section_headers = True
        song = genius.search_song(title, artist)
        await ctx.send(song.lyrics)
