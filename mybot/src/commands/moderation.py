from discord.ext import commands
from MESSAGE_ADMIN import TEXT_admin as text_Admin
from UTILS import get_settings

settings = get_settings()
ownerID = settings['ownerID']

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.guild)  # 5 usos a cada 10 segundos por servidor
    @commands.has_permissions(manage_messages=True)
    async def banWord(self, ctx, *, palavra):
        """
        Adiciona uma palavra à lista de palavras banidas do servidor.\n
        **Parâmetros:**
        - palavra (cadeia): A palavra a ser banida.\n
        **Restrições:**
        - Apenas membros com a permissão ||(Gerenciar mensagems)|| podem usar.
        """
        uid = ctx.author.id
        #if uid == ownerID:
        palavras_ofensivas = text_Admin.get.blacklisted_words()
        if palavra not in palavras_ofensivas:
            text_Admin.save.blacklisted_word(palavras_ofensivas, palavra, uid)
            await ctx.send(f"A palavra '{palavra}' foi adicionada à lista de palavras banidas.")
        else:
            await ctx.send(f"A palavra '{palavra}' já está na lista de palavras banidas.")

    @commands.command()
    @commands.cooldown(2, 8, commands.BucketType.user) # 2 usos a cada 8 segundos por usuario
    async def blackList(self, ctx):
        """
        Lista todas as palavras banidas.
        """
        palavras_banidas = text_Admin.get.blacklisted_words()

        if palavras_banidas:
            mensagem = "\n"
            for palavra in palavras_banidas:
                mensagem += f"- {palavra}\n"
            mensagem += "```"
            await ctx.send("## Palavras banidas")
            await ctx.send(mensagem)
        else:
            await ctx.send("Não há palavras banidas na lista.")


    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.guild)  # 5 usos a cada 10 segundos por servidor
    @commands.has_permissions(manage_messages=True)
    async def cls(self, ctx, número: int):
        """
        Limpa um número específico de mensagens no canal atual.

        **Parâmetros:**
        - número (inteiro): O número de mensagens a serem apagadas.

        **Restrições:**
        - Apenas membros com a permissão ||Gerenciar Mensagens|| podem usar.
        """
        await ctx.channel.purge(limit=número)
        await ctx.send(f'{número} mensagens foram deletadas', delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
