from discord.ext import commands
from UTILS import get_settings
from DATA import COMMAND_data as cmdata

settings = get_settings()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        author = ctx.author
        await ctx.send(f"Olá meu querido, {author.mention} :heart:")

    @commands.command()
    async def menu(self, ctx):
        """
        Envia a página de inicialização e de controle do bot.
        """
        embedMenu, viewMenu = await cmdata.menu(self.bot, settings['prefix'], ctx=ctx)
        await ctx.send(embed=embedMenu, view=viewMenu)


async def setup(bot):
    await bot.add_cog(General(bot))
