import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class MemberBanLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["member_logs"]["bans_kicks"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        log_channel = await self.get_log_channel(guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🔨 Member Banned",
            color=discord.Color.dark_red(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        
        embed.set_author(name=f"{user} (ID: {user.id})", icon_url=user.display_avatar.url)
        
        if guild.me.guild_permissions.view_audit_log:
            async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
                if entry.target.id == user.id:
                    embed.add_field(name="Banned By", value=entry.user.mention, inline=False)
                    if entry.reason:
                        embed.add_field(name="Reason", value=entry.reason, inline=False)
                    break

        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberBanLogger(bot))