import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class PurgeLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["moderation_logs"]["automated_actions"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        if entry.action == discord.AuditLogAction.message_delete:
            log_channel = await self.get_log_channel(entry.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🧹 Messages Purged",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now(datetime.UTC)
            )
            
            embed.add_field(name="Moderator", value=entry.user.mention, inline=True)
            embed.add_field(name="Channel", value=f"<#{entry.extra.channel.id}>", inline=True)
            embed.add_field(name="Messages Deleted", value=entry.extra.count, inline=True)
            
            if entry.reason:
                embed.add_field(name="Reason", value=entry.reason, inline=False)
            
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PurgeLogger(bot))