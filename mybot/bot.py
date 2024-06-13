import sys
import os
import asyncio
import sqlite3

import discord
from discord.ext import commands

from src import command_loader

#===MEUS IMPORTS====INICIO==================================================================
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/text-functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/image-functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data/static'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from UTILS import *
from CONSOLE_RESPONSE import Console
from MESSAGE_ADMIN import TEXT_admin as text_Admin
#===MEUS IMPORTS====FIM=====================================================================
intents = discord.Intents.default()
intents.members = True; intents.message_content = True; intents.guild_messages = True

settings = get_settings()
prefixo = settings['prefix']; ownerID = settings['ownerID']; botToken = settings['botToken']

console = Console()
client = commands.Bot(command_prefix=getPrefix(), intents=intents, owner_id=ownerID)

def iniciar_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE,
                        user_name TEXT
                    )''')
    
    conn.commit()
    conn.close()

def db_add_user(user_id, user_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT OR IGNORE INTO users (user_id, user_name) 
                      VALUES (?, ?)''', (user_id, user_name))
    
    conn.commit()
    conn.close()

def is_bot_owner():
    async def predicate(ctx):
        if ctx.author.id != ctx.bot.owner_id:
            raise commands.NotOwner("Apenas o proprietário do bot pode usar este comando.")
        return True
    return commands.check(predicate)

@client.event
async def on_ready():
    iniciar_db()
    await client.tree.sync()
    console.start(settings)
    await command_loader.load_all(client)

    loaded_successfully = True
    for extension in client.extensions:
        if not client.extensions[extension]:
            loaded_successfully = False
            console.runlog(f"Falha no carregamento do pacote {extension}!")

    if loaded_successfully:
        console.log(f"initload")

class CommandNotFoundError(commands.CommandError):
    def __init__(self, command):
        self.command = command
        super().__init__(f'Comando {command} não encontrado') #repassando mensagem de erro

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFoundError):
        message = await ctx.send(f"🫠 **Comando não encontrado**. Use __**{prefixo}menu**__ para ver a lista de comandos disponíveis.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.CommandNotFound):
        message = await ctx.send(f"🫠 **Comando não encontrado**. Use __**{prefixo}menu**__ para ver a lista de comandos disponíveis.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        message = await ctx.send("🤨 Você não forneceu todos os argumentos necessários. Por favor, verifique o comando e tente novamente.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.BadArgument):
        message = await ctx.send("😶 Um dos argumentos fornecidos é inválido. Por favor, verifique o comando e tente novamente.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.CommandOnCooldown):
        try:
            await ctx.message.delete()
        except discord.errors.DiscordException as e:
            console.log('except', e)
        message = await ctx.send(f"⏳ Este comando está em **cooldown**. Tente novamente em {error.retry_after:.2f} segundos.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.NotOwner):
        message = await ctx.send("🍡 Apenas o proprietário do bot pode usar este comando.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.MissingPermissions):
        message = await ctx.send(f"Você não tem permissão para usar esse comando: __{ctx.command.name}__.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.BotMissingPermissions):
        message = await ctx.send(f"Eu não tenho permissão para usar esse comando: __{ctx.command.name}__.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.DisabledCommand):
        message = await ctx.send("🥲 Este comando está desativado.")
        await asyncio.sleep(10)
        await message.delete()
    elif isinstance(error, commands.CommandInvokeError):
        console.runlog(f"[ERRO] Na execução de um comando: {error}")
        message = await ctx.send(f"😬 Ocorreu um erro ao tentar executar o comando: ||| Uma mensagem foi enviada ao meu criador! ||| Por favor, tente novamente mais tarde.")
        await asyncio.sleep(10)
        await message.delete()
    else:
        console.runlog(f"[ERRO] Na execução de um comando: {error}")
        message = await ctx.send(f"😬 Ocorreu um erro desconhecido: ||| Uma mensagem foi enviada ao meu criador! ||| Por favor, tente novamente mais tarde.")
        await asyncio.sleep(10)
        await message.delete()


@client.command(hidden=True)
@is_bot_owner()
async def load(ctx, extension):
    await client.load_extension(f'src.commands.{extension}')
    await ctx.send(f'{extension} carregado.')

@client.command(hidden=True)
@is_bot_owner()
async def unload(ctx, extension):
    await client.unload_extension(f'src.commands.{extension}')
    await ctx.send(f'{extension} descarregado.')

@client.command(hidden=True)
@is_bot_owner()
async def reload(ctx, extension):
    await client.reload_extension(f'src.commands.{extension}')
    nomeCapitalized = extension.capitalize()
    await ctx.send(f'Olá papis! O pacote **{nomeCapitalized}** foi recarregado.')

@client.command(hidden=True)
@is_bot_owner()
async def sleep(ctx):
    success, response = await console.sleep(ctx)
    await ctx.send(response)
    if success:
        await ctx.bot.close()

@client.command()
async def setprefix(ctx, prefix: str):
    """
    Altera o prefixo do bot para esse servidor.

    **Restrições:**
    - Apenas membros com a permissão ||Administrador|| podem usar.
    """
    uid = ctx.author.id
    success, new_prefix = setPrefix(prefix, uid, ownerID)
    if success:
        global prefixo
        prefixo = new_prefix
        await ctx.send(f"Prefixo atualizado para: '{new_prefix}'")
        console.log('prefix', new_prefix, 'user', ctx.author.name)
    else:
        await ctx.send("Apenas meu dono pode usar esse comando!")

@client.command()
async def list_users(ctx):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id, user_name FROM users')
    rows = cursor.fetchall()
    
    if rows:
        user_list = '\n'.join([f"ID: {row[0]}, Nome: {row[1]}" for row in rows]) #lista de usuarios
        await ctx.send(f"Usuários registrados:\n{user_list}")
    else:
        await ctx.send("Nenhum usuário registrado.")
    
    conn.close()


@client.event
async def on_message(message):
    global prefixo

    if message.author.bot:
        return

    if message.author != client.user:
        client.command_prefix = commands.when_mentioned_or(prefixo)
        
        db_add_user(message.author.id, str(message.author))
        
        if not(text_Admin.get.blacklisted_words(message.content)):
            await client.process_commands(message)
        else:
            verificar = message.content.split()
            if verificar[0] == prefixo+"banWord":
                await client.process_commands(message)
            else:
                console.log('badword', message.author)

                try:
                    await message.delete()
                except discord.errors.Forbidden as e:
                    print(f"O bot não tem permissão para apagar mensagens ofensivas no servidor: {e}")
                    print("Por favor, adicione as permissões necessárias.")
                except Exception as e:
                    print(f"Ocorreu um erro INESPERADO ao tentar apagar a mensagem: {e}")


class CustomHelpCommand(commands.DefaultHelpCommand): #constrói a classe de help customizada
    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(title="Ajuda do Bot", description=f"Use `{self.context.clean_prefix}help [comando]` para obter ajuda sobre um comando específico.", color=discord.Color.red())

        for cog, commands in mapping.items():
            command_list = [command for command in commands if not command.hidden]
            if command_list:
                command_names = "\n".join([f"`{self.get_command_signature(command)}`" for command in command_list])
                embed.add_field(name=cog.qualified_name if cog else "Comandos", value=command_names, inline=False)

        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Ajuda: {command.qualified_name}", color=discord.Color.red())
        embed.add_field(name="Uso", value=f"`{self.get_command_signature(command)}`", inline=False)

        if command.help:
            embed.add_field(name="Descrição", value=command.help, inline=False)
        else:
            embed.add_field(name="Descrição", value="Nenhuma descrição fornecida.", inline=False)

        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        embed = discord.Embed(title=f"Ajuda do {cog.qualified_name}", description=cog.description, color=discord.Color.red())
        for command in cog.get_commands():
            if not command.hidden:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or "Nenhuma descrição fornecida.", inline=False)
        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"Ajuda: {group.qualified_name}", color=discord.Color.red())
        embed.add_field(name="Uso", value=f"`{self.get_command_signature(group)}`", inline=False)

        if group.help:
            embed.add_field(name="Descrição", value=group.help, inline=False)

        subcommands = group.commands
        if subcommands:
            for subcommand in subcommands:
                embed.add_field(name=self.get_command_signature(subcommand), value=subcommand.short_doc or "Nenhuma descrição fornecida.", inline=False)

        await self.context.send(embed=embed)

    async def command_not_found(self, string):
        raise CommandNotFoundError(string)


client.help_command = CustomHelpCommand()
client.get_command('help').help = 'Exibe informações relacionadas ao comando informado'
#^^^^^^^^^^^ Configurando mensagem de help personalizada manualmente, e alterando mensagem padrão de {prefixo}help help

##############
client.run(botToken)
##############