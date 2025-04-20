import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class SafetySettingsLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["server_logs"]["safety_settings"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        changes = []
        
        # Verification level change
        if before.verification_level != after.verification_level:
            levels = ["None", "Low", "Medium", "High", "Highest"]
            changes.append(("Verification Level", 
            levels[before.verification_level.value], 
            levels[after.verification_level.value]))
        
        # Explicit content filter change
        if before.explicit_content_filter != after.explicit_content_filter:
            filters = ["Disabled", "Members without roles", "All members"]
            changes.append(("Content Filter",
            filters[before.explicit_content_filter.value], 
            filters[after.explicit_content_filter.value]))
        
        # Default notifications change
        if before.default_notifications != after.default_notifications:
            notifs = ["All Messages", "Only @mentions"]
            changes.append(("Default Notifications", 
            notifs[before.default_notifications.value], 
            notifs[after.default_notifications.value]))
        
        # MFA level change
        if before.mfa_level != after.mfa_level:
            mfa = ["Disabled", "Enabled"]
            changes.append(("Moderator MFA", 
            mfa[before.mfa_level.value], 
            mfa[after.mfa_level.value]))
        
        # Security level change (community only)
        if hasattr(before, 'security_level') and before.security_level != after.security_level:
            security = ["Off", "Low", "Medium", "High"]
            changes.append(("Security Level", 
            security[before.security_level], 
            security[after.security_level]))
        
        if not changes:
            return

        log_channel = await self.get_log_channel(after.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🛡️ Safety Settings Updated",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        
        for field, before_val, after_val in changes:
            embed.add_field(name=field, value=f"{before_val} → {after_val}", inline=False)
        
        # Check who modified it
        if after.me.guild_permissions.view_audit_log:
            async for entry in after.audit_logs(limit=5, action=discord.AuditLogAction.guild_update):
                embed.add_field(name="Modified By", value=entry.user.mention, inline=False)
                if entry.reason:
                    embed.add_field(name="Reason", value=entry.reason, inline=False)
                break
        
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SafetySettingsLogger(bot))