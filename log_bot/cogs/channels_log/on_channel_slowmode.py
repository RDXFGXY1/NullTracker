import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class ChannelSlowmodeLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["channel_logs"]["slowmode"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.TextChannel):
        if isinstance(after, discord.TextChannel) and before.slowmode_delay != after.slowmode_delay:
            log_channel = await self.get_log_channel(after.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🐢 Slowmode Changed",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="Channel", value=after.mention, inline=False)
            
            before_time = f"{before.slowmode_delay}s" if before.slowmode_delay else "Off"
            after_time = f"{after.slowmode_delay}s" if after.slowmode_delay else "Off"
            embed.add_field(name="Slowmode", value=f"{before_time} → {after_time}", inline=False)
            
            # Check who changed it
            if after.guild.me.guild_permissions.view_audit_log:
                async for entry in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_update):
                    if entry.target.id == after.id:
                        embed.add_field(name="Changed By", value=entry.user.mention, inline=False)
                        if entry.reason:
                            embed.add_field(name="Reason", value=entry.reason, inline=False)
                        break
            
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ChannelSlowmodeLogger(bot))