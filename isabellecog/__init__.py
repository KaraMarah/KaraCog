from .isabellecog import isabellecog

async def setup(bot):
    await bot.add_cog(isabellecog(bot))