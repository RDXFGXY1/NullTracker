import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class ChannelLifecycleLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["channel_logs"]["lifecycle"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        log_channel = await self.get_log_channel(channel.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🆕 Channel Created",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )

        channel_type = str(channel.type).replace("_", " ").title()
        embed.add_field(name="Type", value=channel_type, inline=True)
        embed.add_field(name="Name", value=channel.name, inline=True)
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Position", value=channel.position, inline=True)
        embed.add_field(name="Quick Action", value=f"[Click here](https://discord.com/channels/{channel.guild.id}/{channel.id})")

        if channel.category:
            embed.add_field(name="Category", value=channel.category.name, inline=True)

        # Check who created it
        if channel.guild.me.guild_permissions.view_audit_log:
            async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
                if entry.target.id == channel.id:
                    embed.add_field(name="Created By", value=entry.user.mention, inline=False)
                    if entry.reason:
                        embed.add_field(name="Reason", value=entry.reason, inline=False)
                    break

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        log_channel = await self.get_log_channel(channel.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="❌ Channel Deleted",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )

        channel_type = str(channel.type).replace("_", " ").title()
        embed.add_field(name="Type", value=channel_type, inline=True)
        embed.add_field(name="Name", value=channel.name, inline=True)
        embed.add_field(name="ID", value=channel.id, inline=True)

        if channel.category:
            embed.add_field(name="Category", value=channel.category.name, inline=True)
            

        # Check who deleted it
        if channel.guild.me.guild_permissions.view_audit_log:
            async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_delete):
                if entry.target.id == channel.id:
                    embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
                    if entry.reason:
                        embed.add_field(name="Reason", value=entry.reason, inline=False)
                    break

        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ChannelLifecycleLogger(bot))