import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class ServerAppearanceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["server_logs"]["appearance"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        changes = []
        
        # Server name change
        if before.name != after.name:
            changes.append(("Name", before.name, after.name))
        
        # Server icon change
        if before.icon != after.icon:
            changes.append(("Icon", "Changed", ""))
            if after.icon:
                icon_url = after.icon.url
                changes.append(("New Icon", f"[View]({icon_url})", ""))
        
        # Server banner change
        if before.banner != after.banner:
            changes.append(("Banner", "Changed", ""))
            if after.banner:
                banner_url = after.banner.url
                changes.append(("New Banner", f"[View]({banner_url})", ""))
        
        # Server splash change
        if before.splash != after.splash:
            changes.append(("Splash", "Changed", ""))
            if after.splash:
                splash_url = after.splash.url
                changes.append(("New Splash", f"[View]({splash_url})", ""))
        
        if not changes:
            return

        log_channel = await self.get_log_channel(after.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🎨 Server Appearance Updated",
            color=discord.Color.gold(),
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
    await bot.add_cog(ServerAppearanceLogger(bot))