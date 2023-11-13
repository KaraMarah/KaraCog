from .basecog import BaseCog

async def setup(bot):
    await bot.add_cog(BaseCog(bot))