import discord
from discord.ext import commands
from io import BytesIO

from IMAGE_ADMIN import IMAGE_admin

img = IMAGE_admin()

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user) # 1 uso a cada 20 segundos por usuario
    async def avatar(self, ctx):
        """
        Atualmente apenas para fins de configuração e de testes...
        """
        author = ctx.message.author
        avatar_url = author.avatar.url
        username = author.global_name
        nomeminusculo = username.lower() # Poderia ser upper()
        edited_image = img.draw_menu(avatar_url, nomeminusculo)
        img_bytes = BytesIO()
        edited_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        await ctx.send("Olha só oque nós temos aqui!", file=discord.File(img_bytes, "menu.png"))

async def setup(bot):
    await bot.add_cog(Image(bot))
