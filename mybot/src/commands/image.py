import discord
from discord.ext import commands
from io import BytesIO

from IMAGE_ADMIN import IMAGE_admin as img

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user) # 1 uso a cada 20 segundos por usuario
    async def avatar(self, ctx):
        author = ctx.message.author
        avatar_url = author.avatar.url; username = author.global_name
        usandoOcaso = username.lower() # Poderia ser upper()
        edited_image = img.draw_menu(avatar_url, usandoOcaso)
        img_bytes = BytesIO()
        edited_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        await ctx.send("Olha só oque nós temos aqui!", file=discord.File(img_bytes, "menu.png"))

async def setup(bot):
    await bot.add_cog(Image(bot))
