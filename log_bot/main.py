import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
from dotenv import load_dotenv
from tabulate import tabulate
from colorama import init, Fore, Style, Back

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('NULL_TRACKER_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.presences = True

class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.load_cogs()
        await self.tree.sync()

    async def load_cogs(self):
        for root, dirs, files in os.walk('./cogs'):
            for filename in files:
                if filename.endswith('.py') and filename != "__init__.py":
                    relative_path = os.path.relpath(os.path.join(root, filename), './cogs')
                    module_name = relative_path.replace(os.sep, '.')[:-3]
                    try:
                        await self.load_extension(f'cogs.{module_name}')
                        print(f'{Fore.BLUE}[INFO]\t{Fore.GREEN} Loaded extension: {Style.RESET_ALL} {module_name}')
                    except Exception as e:
                        print(f'{Fore.BLUE}[INFO]\t{Fore.RED} Failed to load extension {Fore.CYAN} {module_name} {Fore.YELLOW} : {type(e).__name__} {Fore.WHITE} - {Back.RED} {e} {Style.RESET_ALL}')

# Initialize bot with custom class
client = CustomBot(
    command_prefix=os.getenv("BOT_PREFIX"),
    intents=discord.Intents.all()
)

@client.event
async def on_ready():
    print(f'Logged in as {Fore.GREEN} {client.user.name} {Style.RESET_ALL} {Fore.YELLOW} ({client.user.id}) {Style.RESET_ALL}')
    # set bot statu to offline
    await client.change_presence(status=discord.Status.online)


if __name__ == "__main__":
    client.run(TOKEN)