import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class VoiceConnectLogger(commands.Cog):
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
        # Member joined a voice channel
        if not before.channel and after.channel:
            log_channel = await self.get_log_channel(member.guild.id)
            if not log_channel:
                return

            embed = discord.Embed(
                title="🎤 Voice Connection",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
            embed.add_field(name="Channel", value=after.channel.mention, inline=False)
            
            if after.self_mute or after.self_deaf:
                status = []
                if after.self_mute:
                    status.append("Self-muted")
                if after.self_deaf:
                    status.append("Self-deafened")
                embed.add_field(name="Status", value=", ".join(status), inline=True)
            
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VoiceConnectLogger(bot))