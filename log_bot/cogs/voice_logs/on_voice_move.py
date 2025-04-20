import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class VoiceMoveLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["voice_logs"]["connections"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # Member moved between channels
        if before.channel and after.channel and before.channel != after.channel:
            log_channel = await self.get_log_channel(member.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🔄 Voice Channel Move",
                color=discord.Color.gold(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
            embed.add_field(name="From", value=before.channel.mention, inline=True)
            embed.add_field(name="To", value=after.channel.mention, inline=True)
            
            # Check if moved by moderator
            if member.guild.me.guild_permissions.view_audit_log:
                async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.member_move):
                    if entry.target.id == member.id:
                        embed.add_field(name="Moved By", value=entry.user.mention, inline=False)
                        if entry.reason:
                            embed.add_field(name="Reason", value=entry.reason, inline=False)
                        break
            
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VoiceMoveLogger(bot))