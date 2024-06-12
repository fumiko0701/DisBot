#=======CONFIGURAÇÕES INICIAS, INICIO ==========
import sys  # usando path para importações OU NÃO
import os  # usando relações de caminho para importações
from src import command_loader  # carrega tudo

import discord
from discord.ext import commands

#===MEUS IMPORTS======================================================================
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/text-functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/image-functions'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data/static'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from UTILS import *
from CONSOLE_RESPONSE import Console
from MESSAGE_ADMIN import TEXT_admin as text_Admin
#===MEUS IMPORTS======================================================================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True

client = commands.Bot(command_prefix=getPrefix(), intents=intents)

settings = get_settings()
prefixo = settings['prefix']  # carreguei o prefixo
ownerID = settings['ownerID']  # id do dono
clientID = settings['clientID']  # carreguei o token

console = Console()  # meu console
#=======CONFIGURAÇÕES INICIAS, FIM ==========

@client.event
async def on_ready():
    await client.tree.sync()
    console.start(settings)
    await command_loader.load_all(client)

    # Verifica se todas as extensões foram carregadas com sucesso
    loaded_successfully = True
    for extension in client.extensions:
        if not client.extensions[extension]:
            loaded_successfully = False
            console.runlog(f"Falha no carregamento do pacote {extension}!")

    if loaded_successfully:
        console.log(f"initload")

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
        await ctx.send(f"Você não tem permissão para executar esse comando: {ctx.command.name}, use `{prefixo}help {ctx.command.name}` para mais informações.", delete_after=10)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"Eu não tenho permissão para executar esse comando: {ctx.command.name}, use `{prefixo}help {ctx.command.name}` para mais informações.", delete_after=10)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("🥲 Este comando está desativado.", delete_after=10)
    elif isinstance(error, commands.CommandInvokeError):
        console.runlog(f"[ERRO] Na execução de um comando: {error}")
        await ctx.send(f"😬 Ocorreu um erro ao tentar executar o comando: ||| Uma mensagem foi enviada ao meu criador! ||| Por favor, tente novamente mais tarde.", delete_after=10)
    else:
        console.runlog(f"[ERRO] Na execução de um comando: {error}")
        await ctx.send(f"😬 Ocorreu um erro desconhecido: ||| Uma mensagem foi enviada ao meu criador! ||| Por favor, tente novamente mais tarde.", delete_after=10)

@client.command(hidden=True)
async def load(ctx, extension):
    await client.load_extension(f'src.commands.{extension}')
    await ctx.send(f'{extension} carregado.')

@client.command(hidden=True)
async def unload(ctx, extension):
    await client.unload_extension(f'src.commands.{extension}')
    await ctx.send(f'{extension} descarregado.')

@client.command(hidden=True)
async def reload(ctx, extension):
    await client.reload_extension(f'src.commands.{extension}')
    await ctx.send(f'{extension} recarregado.')

@client.command()
async def setprefix(ctx, prefix: str):
    uid = ctx.author.id
    success, new_prefix = setPrefix(prefix, uid, ownerID)  # mudando prefixo atual, checando user id e owner id através das settings
    if success:
        global prefixo  # vou alterar a variável global
        prefixo = new_prefix  # atualiza a variável global prefixo através do resultado da setPrefix()
        await ctx.send(f"Prefixo atualizado para: '{new_prefix}'")
        console.log('prefix', new_prefix, 'user', ctx.author.name)  # gera console de alteração de prefixo sucedido
    else:
        await ctx.send("Apenas meu dono pode usar esse comando!")

@client.event
async def on_message(message):
    if message.author.bot:  # ignorando mensagens de outros bots
        return

    if message.author != client.user:
        global prefixo
        client.command_prefix = commands.when_mentioned_or(prefixo)  # muda o prefixo dinamicamente para a mensagem
        if not (text_Admin.get.blacklisted_words(message.content)):  # se não for mensagem banida
            await client.process_commands(message)  # continua lendo
        else:  # se for mensagem banida
            verificar = message.content.split()  # parte a mensagem em pedaços
            if verificar[0] == prefixo + "banWord":  # verifica se ela é o comando de banir palavras
                await client.process_commands(message)  # se for, continua lendo
            else:  # se não for, realmente bloqueia a mensagem
                console.log('badword', message.author)  # posso passar True ou False como um ultimo parametro, para mensagem especial
                try:
                    await message.delete()
                except discord.errors.Forbidden as e:
                    print(f"O bot não tem permissão para apagar mensagens ofensivas no servidor: {e}")
                    print("Por favor, adicione as permissões necessárias.")
                except Exception as e:
                    print(f"Ocorreu um erro INESPERADO ao tentar apagar a mensagem: {e}")

# Custom help command to display help for setprefix command
class CustomHelpCommand(commands.DefaultHelpCommand):
    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    async def send_bot_help(self, mapping):
        # Override this to customize help for the entire bot
        ctx = self.context
        embed = discord.Embed(title="Ajuda do Bot", description="Lista de comandos disponíveis:", color=discord.Color.blue())
        for cog, commands in mapping.items():
            command_list = [command for command in commands if not command.hidden]
            if command_list:
                command_names = "\n".join([f"`{self.get_command_signature(command)}`" for command in command_list])
                embed.add_field(name=cog.qualified_name if cog else "Comandos", value=command_names, inline=False)
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        if command.name == "setprefix":
            embed = discord.Embed(title="Ajuda: setprefix", description="Altera o prefixo de comandos do bot.", color=discord.Color.blue())
            embed.add_field(name="Uso", value=f"`{self.context.clean_prefix}setprefix <novo_prefixo>`", inline=False)
            embed.add_field(name="Exemplo", value=f"`{self.context.clean_prefix}setprefix !`", inline=False)
            embed.add_field(name="Descrição", value="Somente o dono do bot pode alterar o prefixo.", inline=False)
            await self.context.send(embed=embed)
        else:
            await super().send_command_help(command)

client.help_command = CustomHelpCommand()

client.run(clientID)  # fim da linha, vou ter que rodar, huehuehuehe
