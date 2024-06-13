import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Pong!
        """
        await ctx.send("Pong!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
