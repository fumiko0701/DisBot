import discord
from discord.ext import commands

from UTILS import *
settings = get_settings()
ownerID = settings['ownerID']

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await member.add_roles(role)
            await ctx.send(f'{role.name} foi adicionado a {member.mention}')
        else:
            await ctx.send("Você não tem permissão para usar este comando.")

    @commands.command()
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await member.remove_roles(role)
            await ctx.send(f'{role.name} foi removido de {member.mention}')
        else:
            await ctx.send("Você não tem permissão para usar este comando.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
