import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class ModerationLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.action_icons = {
            'ban': '🔨',
            'unban': '🔓',
            'kick': '👢',
            'mute': '🔇',
            'unmute': '🔊',
            'warn': '⚠️',
            'timeout': '⏳'
        }

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["moderation_logs"]["automated_actions"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    async def log_mod_action(self, action_type: str, moderator: discord.Member, 
                           target: discord.User, reason: str = None, **kwargs):
        log_channel = await self.get_log_channel(moderator.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title=f"{self.action_icons.get(action_type, '⚖️')} {action_type.title()}",
            color=self.get_action_color(action_type),
            timestamp=datetime.datetime.now(datetime.UTC)
        )

        embed.add_field(name="Moderator", value=moderator.mention, inline=True)
        embed.add_field(name="Target", value=f"{target} (ID: {target.id})", inline=True)
        
        if duration := kwargs.get('duration'):
            embed.add_field(name="Duration", value=duration, inline=True)
        
        if reason:
            embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        
        if proof := kwargs.get('proof'):
            embed.add_field(name="Proof", value=proof, inline=False)

        await log_channel.send(embed=embed)

    def get_action_color(self, action_type: str) -> discord.Color:
        colors = {
            'ban': discord.Color.red(),
            'unban': discord.Color.green(),
            'kick': discord.Color.orange(),
            'mute': discord.Color.dark_grey(),
            'unmute': discord.Color.green(),
            'warn': discord.Color.gold(),
            'timeout': discord.Color.dark_blue()
        }
        return colors.get(action_type, discord.Color.blurple())

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id:
                await self.log_mod_action(
                    action_type="ban",
                    moderator=entry.user,
                    target=user,
                    reason=entry.reason
                )
                break

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.unban):
            if entry.target.id == user.id:
                await self.log_mod_action(
                    action_type="unban",
                    moderator=entry.user,
                    target=user,
                    reason=entry.reason
                )
                break

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        if entry.action == discord.AuditLogAction.kick:
            await self.log_mod_action(
                action_type="kick",
                moderator=entry.user,
                target=entry.target,
                reason=entry.reason
            )
        elif entry.action == discord.AuditLogAction.member_update:
            if hasattr(entry.extra, 'timed_out_until'):
                action = "timeout" if entry.extra.timed_out_until else "unmute"
                now = datetime.datetime.now(datetime.UTC)
                await self.log_mod_action(
                    action_type=action,
                    moderator=entry.user,
                    target=entry.target,
                    reason=entry.reason,
                    duration=str(entry.extra.timed_out_until - now) if action == "timeout" else None
                )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Issue a warning to a member"""
        await self.log_mod_action(
            action_type="warn",
            moderator=ctx.author,
            target=member,
            reason=reason,
            proof=f"[Jump to warning]({ctx.message.jump_url})"
        )
        await ctx.send(f"⚠️ Warning issued to {member.mention}")

async def setup(bot):
    await bot.add_cog(ModerationLogger(bot))