import os
from discord.ext import commands

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'data/static'))
from data.static.CONSOLE_RESPONSE import Console

console = Console()

async def load_all(bot: commands.Bot):
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            extension = f"src.commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                console.runlog(f"Loaded extension: {extension}")
            except Exception as e:
                console.runlog(f"Failed to load extension {extension}: {e}")
