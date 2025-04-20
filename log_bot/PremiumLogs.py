import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import csv
import time
import matplotlib.pyplot as plt
from io import BytesIO
from typing import List, Dict, Optional

class PremiumLoggingSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_stats = {}
        self.filters = self.load_filters()
        self.central_log_channel = None  # Set this to your admin server channel ID
        self.backup_interval = 3600  # 1 hour in seconds
        self.backup_task.start()

    def cog_unload(self):
        self.backup_task.cancel()

    """Feature 1: Log Channel Verification"""
    async def verify_channel(self, channel: discord.TextChannel) -> bool:
        perms = channel.permissions_for(channel.guild.me)
        return all([
            perms.send_messages,
            perms.embed_links,
            perms.attach_files,
            perms.read_message_history
        ])

    @app_commands.command(name="verifylog")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def verify_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Check if a channel is suitable for logging"""
        is_valid = await self.verify_channel(channel)
        embed = discord.Embed(
            title="🔍 Channel Verification",
            color=0x00ff00 if is_valid else 0xff0000,
            description=f"{channel.mention} is {'✅ VALID' if is_valid else '❌ INVALID'} for logging"
        )
        
        if not is_valid:
            embed.add_field(
                name="Missing Permissions",
                value="The bot needs:\n- Send Messages\n- Embed Links\n- Attach Files\n- Read Message History",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    """Feature 2: Centralized Log Forwarding"""
    @app_commands.command(name="setcentral")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_central_log(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set central logging channel (admin only)"""
        self.central_log_channel = channel.id
        await interaction.response.send_message(
            f"✅ All logs will be forwarded to {channel.mention}",
            ephemeral=True
        )

    async def forward_to_central(self, embed: discord.Embed):
        if self.central_log_channel:
            channel = self.bot.get_channel(self.central_log_channel)
            if channel:
                await channel.send(embed=embed)

    """Feature 3: Dynamic Log Filtering"""
    def load_filters(self) -> Dict[int, List[str]]:
        try:
            with open('data/log_filters.json', 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_filters(self):
        with open('data/log_filters.json', 'w') as f:
            json.dump(self.filters, f)

    @app_commands.command(name="logfilter")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def manage_filters(
        self,
        interaction: discord.Interaction,
        action: str,
        keyword: str
    ):
        """Add/remove log filters (prevents logging sensitive info)"""
        guild_id = str(interaction.guild.id)
        
        if action == "add":
            if guild_id not in self.filters:
                self.filters[guild_id] = []
            if keyword not in self.filters[guild_id]:
                self.filters[guild_id].append(keyword)
                msg = f"✅ Added filter: `{keyword}`"
            else:
                msg = f"⚠️ Filter already exists: `{keyword}`"
        
        elif action == "remove":
            if guild_id in self.filters and keyword in self.filters[guild_id]:
                self.filters[guild_id].remove(keyword)
                msg = f"✅ Removed filter: `{keyword}`"
            else:
                msg = f"⚠️ Filter not found: `{keyword}`"
        
        self.save_filters()
        await interaction.response.send_message(msg, ephemeral=True)

    def is_filtered(self, guild_id: int, content: str) -> bool:
        filters = self.filters.get(str(guild_id), [])
        return any(f.lower() in content.lower() for f in filters)

    """Feature 4: Log Statistics Dashboard"""
    def update_stats(self, log_type: str):
        self.log_stats[log_type] = self.log_stats.get(log_type, 0) + 1

    @app_commands.command(name="logstats")
    async def show_statistics(self, interaction: discord.Interaction, days: int = 7):
        """Generate log statistics visualization"""
        # Generate chart
        plt.figure(figsize=(10, 6))
        types, counts = zip(*sorted(self.log_stats.items()))
        plt.bar(types, counts, color='skyblue')
        plt.title(f"Log Activity (Last {days} Days)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save to bytes
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        # Send
        file = discord.File(buffer, filename="log_stats.png")
        embed = discord.Embed(title="📊 Log Statistics", color=0x3498db)
        embed.set_image(url="attachment://log_stats.png")
        await interaction.response.send_message(embed=embed, file=file)

    """Feature 5: One-Click Log Export"""
    @app_commands.command(name="exportlogs")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def export_logs(self, interaction: discord.Interaction):
        """Export all logs to CSV"""
        # Load logs (you'll need to implement your log storage system)
        logs = self.load_logs(interaction.guild.id)
        
        # Create CSV
        with open('logs_export.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', 'Type', 'User', 'Action'])
            for log in logs:
                writer.writerow(log)
        
        # Send file
        file = discord.File('logs_export.csv')
        await interaction.response.send_message(
            "📁 Here's your log export:",
            file=file,
            ephemeral=True
        )

    """Background Tasks"""
    @tasks.loop(seconds=3600)
    async def backup_task(self):
        for guild in self.bot.guilds:
            try:
                shutil.copy2(
                    f"servers/logs/{guild.id}.json",
                    f"servers/backups/{guild.id}_{int(time.time())}.json"
                )
            except:
                continue

async def setup(bot):
    await bot.add_cog(PremiumLoggingSystem(bot))