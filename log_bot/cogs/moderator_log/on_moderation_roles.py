import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class ModerationRoleLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["moderation_logs"]["automated_actions"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # Check for moderator role changes
        mod_roles = [r for r in after.guild.roles if r.permissions.manage_messages]
        
        added = [r for r in after.roles if r not in before.roles and r in mod_roles]
        removed = [r for r in before.roles if r not in after.roles and r in mod_roles]
        
        if not added and not removed:
            return

        log_channel = await self.get_log_channel(after.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🛡️ Moderator Role Update",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        
        embed.add_field(name="Member", value=f"{after} (ID: {after.id})", inline=False)
        
        if added:
            embed.add_field(name="Roles Added", value="\n".join(r.mention for r in added), inline=False)
        if removed:
            embed.add_field(name="Roles Removed", value="\n".join(r.mention for r in removed), inline=False)
        
        # Check who modified roles
        if after.guild.me.guild_permissions.view_audit_log:
            async for entry in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.member_role_update):
                if entry.target.id == after.id:
                    embed.add_field(name="Modified By", value=entry.user.mention, inline=False)
                    if entry.reason:
                        embed.add_field(name="Reason", value=entry.reason, inline=False)
                    break
        
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ModerationRoleLogger(bot))