from .GeniusCog import GeniusCog

async def setup(bot):
    await bot.add_cog(GeniusCog(bot))
