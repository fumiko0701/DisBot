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
        embedMenu, viewMenu = await cmdata.menu(self.bot, settings['prefix'], ctx=ctx)
        await ctx.send(embed=embedMenu, view=viewMenu)

    @commands.command()
    async def list_commands(self, ctx):  # Adicione 'self' como o primeiro argumento
        # Inicialize um dicionário para armazenar os comandos por categoria
        command_dict = {}

        # Preencha o dicionário com os comandos e suas categorias
        for cog_name, cog in self.bot.cogs.items():  # Use 'self.bot' em vez de 'bot'
            for command in cog.get_commands():
                # Verifica se o comando tem uma categoria definida
                if hasattr(command.cog, 'qualified_name'):
                    category = command.cog.qualified_name
                else:
                    category = "Sem categoria"
                # Adiciona o comando ao dicionário
                if category not in command_dict:
                    command_dict[category] = []
                command_dict[category].append(command.name)

        # Cria uma mensagem com os comandos por categoria
        message = "Lista de comandos por categoria:\n"
        for category, commands in command_dict.items():
            message += f"**{category}**:\n"
            message += ", ".join(commands) + "\n"

        # Envia a mensagem para o canal
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(General(bot))
