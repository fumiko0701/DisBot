                    #=======CONFIGURAÇÕES INICIAS, INICIO ==========
import asyncio
import json
import sys #usando path para importações OU NÃO
import os #usando relações de caminho para importações
from io import BytesIO
import aiohttp

import discord
from discord.ext import commands

#===MEUS IMPORTS======================================================================
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/text-functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/image-functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data/static'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from IMAGE_ADMIN import IMAGE_admin
from DATA import COMMAND_data
from MESSAGE_ADMIN import TEXT_admin
from UPDATER import *
from UPDATER import CommandList
from CONSOLE_RESPONSE import Console
#===MEUS IMPORTS======================================================================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True

client = commands.Bot(command_prefix=getPrefix(), intents=intents)

caminho_settings = os.path.join(os.path.dirname(__file__), 'data/static/settings.json')
with open(caminho_settings, 'r') as settings_file: #carregando as configurações
    settings = json.load(settings_file) #peguei a lista e as chaves das settings
prefixo = settings['prefix'] #carreguei o prefixo
ownerID = settings['ownerID'] #id do dono
clientID = settings['clientID'] #carreguei o token

console = Console() #meu console
text_Admin = TEXT_admin(); """meu administrador de texto"""; img = IMAGE_admin() #controlador de imagens
cmdata = COMMAND_data(); """#data e formatação de respostas de comandos e/embeds"""; incmdlist = CommandList() #lista de comandos
                    #=======CONFIGURAÇÕES INICIAS, FIM ==========

#dicas: usar os comandos do UPDATER.py dentro do CONSOLE_RESPONSES, na classe Console, ou em outra classe...

#dica contraria: manter a classe console somente responsavel pela documentação dos processos, exemplo: salvar items ou modificar items,
#e também responsavel pela demonstração de erros, logo evitando ser responsavel pela alteração de bases importantes.

@client.event
async def on_ready():
    await client.tree.sync()
    console.start(settings)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"🫠 **Comando não encontrado**. Use __**{prefixo}menu**__ para ver a lista de comandos disponíveis.", delete_after=10)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("🤨 Você não forneceu todos os argumentos necessários. Por favor, verifique o comando e tente novamente.", delete_after=10)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("😶 Um dos argumentos fornecidos é inválido. Por favor, verifique o comando e tente novamente.", delete_after=10)
    elif isinstance(error, commands.CommandOnCooldown):
        try:
            await ctx.message.delete()
        except discord.errors.DiscordException as e:
            console.log('except', e)
        await ctx.send(f"⏳ Este comando está em **cooldown**. Tente novamente em {error.retry_after:.2f} segundos.", delete_after=10)
    elif isinstance(error, commands.NotOwner):
        await ctx.send("🍡 Apenas o proprietário do bot pode usar este comando.", delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🙁 Você não tem as permissões necessárias para usar este comando.", delete_after=10)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("😿 Eu não tenho as permissões necessárias para executar este comando.", delete_after=10)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("🥲 Este comando está desativado.", delete_after=10)
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"😬 Ocorreu um erro ao tentar executar o comando: ||| {error} ||| Por favor, tente novamente mais tarde.", delete_after=10)
    else:
        await ctx.send(f"😬 Ocorreu um erro desconhecido: ||| {error} ||| Por favor, tente novamente mais tarde.", delete_after=10)


@client.command()
async def sleep(ctx):
    #await console.sleep(ctx, ownerID)
    await discord.ext.commands.Bot.close
    await discord.Client.close(self=client)


#============= AREA PARA TESTES DE NOVOS COMANDOS

@client.command()
async def cmdlist(ctx):

    await ctx.send("Chequei")
 

#============= AREA PARA TESTES DE NOVOS COMANDOS

@client.command()
async def setprefix(ctx, prefix: str):
    uid = ctx.author.id
    success, new_prefix = setPrefix(prefix, uid, ownerID, settings) #mudando prefixo atual, checando user id e owner id através das settings
    if success:
        global prefixo #vou alterar a variável global
        prefixo = new_prefix#atualiza a variável global prefixo através do resultado da setprefix()
        await ctx.send(f"Prefixo atualizado para: ' {new_prefix} '")
        console.log('prefix', new_prefix, 'user', ctx.author.name)#gera console de alteração de prefix sucedido
    else:
        await ctx.send("Apenas meu dono pode usar esse comando!")

"""------------------------------------------------------------------------------------------------------MENU"""
#prefix_command(menu)
@client.command()
@commands.cooldown(2, 10, commands.BucketType.user) #2 usos a cada 10 segundos por usuario
async def menu(ctx):

    embedMenu, viewMenu = cmdata.get.menu(client, prefixo, ctx=ctx)
    await ctx.send(embed=embedMenu, view=viewMenu) 
    
#slash_command(menu)
@client.tree.command(name="menu", description="Guia rápido com alguns exemplares de comandos...")
@commands.cooldown(2, 10, commands.BucketType.user) #2 usos a cada 10 segundos por usuario
async def slash_command(interaction: discord.Interaction):
    embedMenu, viewMenu = cmdata.get.menu(client, prefixo, interaction=interaction)
    await interaction.response.send_message(embed=embedMenu, view=viewMenu, ephemeral=True) 
"""------------------------------------------------------------------------------------------------------MENU"""

@client.command()
async def hi(ctx):
    author = ctx.author
    await ctx.send(f"Olá meu querido, {author.mention} :heart:")


@client.command()
@commands.cooldown(1, 20, commands.BucketType.user) #1 uso a cada 20 segundos por usuario
async def avatar(ctx):

    author = ctx.message.author

    avatar_url = author.avatar.url; username = author.global_name

    usandoOcaso = username.lower() #Poderia ser upper()

#metodo img.draw da classe IMAGE_admin na image-functions
    edited_image = img.draw_menu(avatar_url, usandoOcaso)

#converte a imagem editada
    img_bytes = BytesIO()
    edited_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    #envia mensagem
    await ctx.send("Olha só oque nós temos aqui!", file=discord.File(img_bytes, "menu.png"))


@client.command()
@commands.cooldown(5, 10, commands.BucketType.guild) #5 uso a cada 10 segundos por servidor
async def cls(ctx, num: int):
    await ctx.channel.purge(limit=num+1)
    await ctx.send(f"🧹 **Limpinho!** | {num} {'mensagems foram apagadas!' if num > 1 else 'mensagem foi apagada!'}", delete_after=5)


@client.command()
@commands.cooldown(6, 10, commands.BucketType.user) #6 usos a cada 10 segundos por usuario
async def banWord(ctx, *, word):
    uid = ctx.author.id  # pegar o id do usuário
    if uid == ownerID:  # se o usuário for o dono
        palavras_ofensivas = text_Admin.get.blacklisted_words() # PALAVRAS PROIBIDAS
        if word not in palavras_ofensivas:  # se a nova palavra não estiver na lista
            text_Admin.save.blacklisted_word(palavras_ofensivas, word, uid)  #salvando a palavra proibida
            await ctx.send(f"A palavra '{word}' foi adicionada à lista de palavras banidas.")
        else:  # se a palavra já estiver na lista
            await ctx.send(f"A palavra '{word}' já está na lista de palavras banidas.")
    else:
        await ctx.send("Você não tem permissão para usar este comando.")


@client.command()
@commands.cooldown(2, 8, commands.BucketType.user) #2 usos a cada 8 segundos por usuario
async def blackList(ctx):
    palavras_banidas = text_Admin.get.blacklisted_words() #peguei as palavras banidas huehuehue

    if palavras_banidas:
        #vou tentar formatar como código msm
        mensagem = "\n"
        for palavra in palavras_banidas: #para cada palavra na lista
            mensagem += f"- {palavra}\n" #vou adicionar no começo e no fim 
        mensagem += "```"
        await ctx.send("## Palavras banidas")
        await ctx.send(mensagem)
    else:
        await ctx.send("Não há palavras banidas na lista.")

@client.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    incmdlist.check('membergest', 'mute')
    # Verificar se o autor do comando tem permissão para gerenciar cargos
    if ctx.author.guild_permissions.manage_roles:
        # Verificar se o cargo "Muted" já existe
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        # Se o cargo "Muted" não existir, criá-lo e definir permissões nos canais
        if not mute_role:
            try:
                mute_role = await ctx.guild.create_role(name="Muted")

                for channel in ctx.guild.channels:
                    await channel.set_permissions(mute_role, speak=False, send_messages=False)
            except discord.Forbidden:
                await ctx.send("O bot não tem permissão para criar cargos ou definir permissões nos canais.")
                return

        # Adicionar o cargo "Muted" ao usuário especificado
        try:
            await member.add_roles(mute_role, reason=reason)
            await ctx.send(f'{member.mention} foi mutado por {reason}')
        except discord.Forbidden:
            await ctx.send("O bot não tem permissão para gerenciar cargos.")
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def unmute(ctx, member: discord.Member):
    incmdlist.check('membergest', 'unmute')
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f'{member.mention} foi desmutado')
        else:
            await ctx.send(f'{member.mention} não está mutado')
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    incmdlist.check('membergest', 'kick')
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} foi expulso por {reason}')
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    incmdlist.check('membergest', 'ban')
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} foi banido por {reason}')
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def unban(ctx, *, member):
    incmdlist.check('membergest', 'unban')
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} foi desbanido')
                return

        await ctx.send(f'{member} não foi encontrado')
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def clear(ctx, amount=5):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} mensagens foram deletadas', delete_after=5)
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        await member.add_roles(role)
        await ctx.send(f'{role.name} foi adicionado a {member.mention}')
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        await member.remove_roles(role)
        await ctx.send(f'{role.name} foi removido de {member.mention}')
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

@client.command()
async def oi(ctx):
    await ctx.send("Hello. ~From C")


@client.event
async def on_message(message):
    global prefixo

    if message.author.bot: #ignorando mensagems de outros bots
        return

    if message.author != client.user:
        global prefixo
        #if message.content.startswith(prefixo): #verifica o prefixo                                          #AINDA PRECISO DISSO?
        client.command_prefix = commands.when_mentioned_or(prefixo) #muda o prefixo dinamicamente para a mensagem #AINDA PRECISO DISSO?
        if not(text_Admin.get.blacklisted_words(message.content)): # se não for mensagem banida
            await client.process_commands(message) #continua lendo
        else: #se for mensagem banida
            verificar = message.content.split() #parte a mensagem em pedaços
            if verificar[0] == prefixo+"banWord": #verifica se ela é o comando de banir palavras
                await client.process_commands(message) #se for, continua lendo
            else: # se não for, realmente bloqueia a mensagem
                console.log('badword', message.author) #posso passar True ou False como um ultimo parametro, para mensagem especial
                
                try:
                    await message.delete()
                except discord.errors.Forbidden as e:
                    print(f"O bot não tem permissão para apagar mensagens ofensivas no servidor: {e}")
                    print("Por favor, adicione as permissões necessárias.")
                except Exception as e:
                    print(f"Ocorreu um erro INESPERADO ao tentar apagar a mensagem: {e}")


    
client.run(clientID) #fim da linha, vou ter que rodar, huehuehuehe
