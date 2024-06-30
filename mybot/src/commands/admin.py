import discord
from discord.ext import commands

from UTILS import *
settings = get_settings()
ownerID = settings['ownerID']

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def addrole(self, ctx, membro: discord.Member, cargo: discord.Role):
        """
        In-built command

        Adiciona um cargo do servidor fornecido ao membro fornecido.
        """
        if ctx.author.guild_permissions.manage_roles:
            await membro.add_roles(cargo)
            await ctx.send(f'{cargo.name} foi adicionado a {membro.mention}')
        else:
            await ctx.send("Você não tem permissão para usar este comando.")

    @commands.command()
    async def removerole(self, ctx, membro: discord.Member, cargo: discord.Role):
        """
        In-built command

        Remove um cargo do servidor inserido do membro fornecido.
        """
        if ctx.author.guild_permissions.manage_roles:
            await membro.remove_roles(cargo)
            await ctx.send(f'{cargo.name} foi removido de {membro.mention}')
        else:
            await ctx.send("Você não tem permissão para usar este comando.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
