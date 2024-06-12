from discord.ext import commands

from MESSAGE_ADMIN import TEXT_admin as text_Admin
from UTILS import get_settings
settings = get_settings()
ownerID = settings['ownerID']

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(6, 10, commands.BucketType.user) # 6 usos a cada 10 segundos por usuario
    async def banWord(self, ctx, *, word):
        uid = ctx.author.id  # pegar o id do usuário
        if uid == ownerID:  # se o usuário for o dono
            palavras_ofensivas = text_Admin.get.blacklisted_words() # PALAVRAS PROIBIDAS
            if word not in palavras_ofensivas:  # se a nova palavra não estiver na lista
                text_Admin.save.blacklisted_word(palavras_ofensivas, word, uid)  # salvando a palavra proibida
                await ctx.send(f"A palavra '{word}' foi adicionada à lista de palavras banidas.")
            else:  # se a palavra já estiver na lista
                await ctx.send(f"A palavra '{word}' já está na lista de palavras banidas.")
        else:
            await ctx.send("Você não tem permissão para usar este comando.")

    @commands.command()
    @commands.cooldown(2, 8, commands.BucketType.user) # 2 usos a cada 8 segundos por usuario
    async def blackList(self, ctx):
        palavras_banidas = text_Admin.get.blacklisted_words() # peguei as palavras banidas huehuehue

        if palavras_banidas:
            # vou tentar formatar como código msm
            mensagem = "\n"
            for palavra in palavras_banidas: # para cada palavra na lista
                mensagem += f"- {palavra}\n" # vou adicionar no começo e no fim 
            mensagem += "```"
            await ctx.send("## Palavras banidas")
            await ctx.send(mensagem)
        else:
            await ctx.send("Não há palavras banidas na lista.")

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.guild) # 5 uso a cada 10 segundos por servidor
    async def cls(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        await ctx.send(f"🧹 **Limpinho!** | {num} {'mensagems foram apagadas!' if num > 1 else 'mensagem foi apagada!'}", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
