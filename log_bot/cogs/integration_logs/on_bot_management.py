import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class BotManagementLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["integration_logs"]["bot_management"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            log_channel = await self.get_log_channel(member.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🤖 Bot Added",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
            
            # Check who added the bot
            if member.guild.me.guild_permissions.view_audit_log:
                async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.bot_add):
                    if entry.target.id == member.id:
                        embed.add_field(name="Added By", value=entry.user.mention, inline=False)
                        if entry.reason:
                            embed.add_field(name="Reason", value=entry.reason, inline=False)
                        break

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.bot:
            log_channel = await self.get_log_channel(member.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🚫 Bot Removed",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
            
            # Check who removed the bot
            if member.guild.me.guild_permissions.view_audit_log:
                async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
                    if entry.target.id == member.id:
                        embed.add_field(name="Removed By", value=entry.user.mention, inline=False)
                        if entry.reason:
                            embed.add_field(name="Reason", value=entry.reason, inline=False)
                        break

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        if entry.action == discord.AuditLogAction.bot_add and not getattr(entry.target, 'bot', True):
            # Handle cases where a user account is converted to a bot
            log_channel = await self.get_log_channel(entry.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🔄 User Converted to Bot",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_author(name=f"{entry.target} (ID: {entry.target.id})", icon_url=entry.target.display_avatar.url)
            embed.add_field(name="Action By", value=entry.user.mention, inline=False)
            
            if entry.reason:
                embed.add_field(name="Reason", value=entry.reason, inline=False)

            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotManagementLogger(bot))