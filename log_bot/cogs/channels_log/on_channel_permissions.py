import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class ChannelPermissionsLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["channel_logs"]["permissions"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if before.overwrites != after.overwrites:
            log_channel = await self.get_log_channel(after.guild.id)
            if not log_channel:
                return

            # Get permission changes
            changes = []
            all_targets = set(before.overwrites.keys()) | set(after.overwrites.keys())
            
            for target in all_targets:
                before_overwrite = before.overwrites.get(target)
                after_overwrite = after.overwrites.get(target)
                
                if before_overwrite != after_overwrite:
                    target_name = target.mention if isinstance(target, (discord.Role, discord.Member)) else str(target)
                    changes.append(f"**{target_name}**")
                    
                    if before_overwrite and after_overwrite:
                        # Changed permissions
                        for perm, value in after_overwrite:
                            if getattr(before_overwrite, perm) != value:
                                changes.append(f"- {perm}: {'✅' if value else '❌'}")
                    elif after_overwrite:
                        # New overwrite
                        changes.append("- New permissions set")
                    else:
                        # Removed overwrite
                        changes.append("- Permissions reset")

            if changes:
                embed = discord.Embed(
                    title="🔐 Channel Permissions Updated",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now()
                )
                
                embed.add_field(name="Channel", value=after.mention, inline=False)
                embed.add_field(name="Changes", value="\n".join(changes), inline=False)
                
                # Check who modified it
                if after.guild.me.guild_permissions.view_audit_log:
                    async for entry in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.overwrite_update):
                        if entry.target.id == after.id:
                            embed.add_field(name="Modified By", value=entry.user.mention, inline=False)
                            if entry.reason:
                                embed.add_field(name="Reason", value=entry.reason, inline=False)
                            break
                
                await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ChannelPermissionsLogger(bot))
