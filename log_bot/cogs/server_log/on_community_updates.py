import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class CommunityUpdatesLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["server_logs"]["community_updates"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        changes = []
        
        # Community status change
        if before.features != after.features:
            new_features = set(after.features) - set(before.features)
            removed_features = set(before.features) - set(after.features)
            
            if new_features:
                changes.append(("Features Added", ", ".join(new_features), ""))
            if removed_features:
                changes.append(("Features Removed", ", ".join(removed_features), ""))
        
        # Rules channel change
        if before.rules_channel != after.rules_channel:
            changes.append(("Rules Channel", before.rules_channel.mention if before.rules_channel else "None", after.rules_channel.mention if after.rules_channel else "None"))
        
        # Community updates channel change
        if before.public_updates_channel != after.public_updates_channel:
            changes.append(("Updates Channel", before.public_updates_channel.mention if before.public_updates_channel else "None", after.public_updates_channel.mention if after.public_updates_channel else "None"))
        
        # Description change
        if before.description != after.description:
            old_desc = before.description or "None"
            new_desc = after.description or "None"
            changes.append(("Description", f"{old_desc[:100]}..." if len(old_desc) > 100 else f"{old_desc}", f"{new_desc[:100]}..." if len(new_desc) > 100 else f"{new_desc}"))
        
        if not changes:
            return

        log_channel = await self.get_log_channel(after.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="📢 Community Updates",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        
        for field, before_val, after_val in changes:
            if before_val and after_val:
                embed.add_field(name=field, value=f"{before_val} → {after_val}", inline=False)
            else:
                embed.add_field(name=field, value=before_val or after_val, inline=False)
        
        # Check who modified it
        if after.me.guild_permissions.view_audit_log:
            async for entry in after.audit_logs(limit=5, action=discord.AuditLogAction.guild_update):
                embed.add_field(name="Modified By", value=entry.user.mention, inline=False)
                if entry.reason:
                    embed.add_field(name="Reason", value=entry.reason, inline=False)
                break
        
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommunityUpdatesLogger(bot))