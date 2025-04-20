import discord
from discord.ext import commands
import json
import datetime
from typing import Optional


class MemberJoinLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                channel_id = config["member_logs"]["join_leave"]["channel_id"]
                if channel_id:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        log_channel = await self.get_log_channel(member.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🟢 Member Joined",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        
        embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
        
        account_age = (datetime.datetime.now(datetime.UTC) - member.created_at).days
        embed.add_field(name="Account Age", value=f"{account_age} days", inline=True)
        
        embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)
        
        if member.guild.me.guild_permissions.view_audit_log:
            async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.bot_add):
                if entry.target.id == member.id:
                    embed.add_field(name="Added By", value=entry.user.mention, inline=False)
                    break

        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberJoinLogger(bot))