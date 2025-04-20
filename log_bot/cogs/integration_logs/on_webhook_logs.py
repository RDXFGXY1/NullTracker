import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class WebhookLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["integration_logs"]["webhooks"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.TextChannel):
        log_channel = await self.get_log_channel(channel.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🪝 Webhook Activity",
            color=discord.Color.purple(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        
        # Check audit log for details
        if channel.guild.me.guild_permissions.view_audit_log:
            async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.webhook_create):
                if getattr(entry.extra, 'channel', None) and entry.extra.channel.id == channel.id:
                    embed.add_field(name="Created By", value=entry.user.mention, inline=False)
                    if entry.reason:
                        embed.add_field(name="Reason", value=entry.reason, inline=False)
                    break

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        if entry.action in (discord.AuditLogAction.webhook_create, discord.AuditLogAction.webhook_update, discord.AuditLogAction.webhook_delete):
            
            log_channel = await self.get_log_channel(entry.guild.id)
            if not log_channel:
                return

            action_emoji = {
                discord.AuditLogAction.webhook_create: "🆕",
                discord.AuditLogAction.webhook_update: "✏️",
                discord.AuditLogAction.webhook_delete: "❌"
            }.get(entry.action, "ℹ️")

            embed = discord.Embed(
                title=f"{action_emoji} Webhook {entry.action.name.split('_')[-1].title()}",
                color=discord.Color.purple(),
                timestamp=datetime.datetime.now()
            )
            
            if entry.target and hasattr(entry.target, 'name') and hasattr(entry.target, 'id'):
                embed.add_field(name="Webhook", value=f"{entry.target.name} (ID: {entry.target.id})", inline=False)
            
            if getattr(entry.extra, 'channel', None):
                embed.add_field(name="Channel", value=entry.extra.channel.mention, inline=True)
            
            embed.add_field(name="Action By", value=entry.user.mention, inline=False)
            
            if entry.reason:
                embed.add_field(name="Reason", value=entry.reason, inline=False)

            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WebhookLogger(bot))