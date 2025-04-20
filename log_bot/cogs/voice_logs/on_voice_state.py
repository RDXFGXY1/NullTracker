import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class VoiceStateLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["voice_logs"]["state_changes"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # Skip if no channel change
        if before.channel == after.channel:
            log_channel = await self.get_log_channel(member.guild.id)
            if not log_channel:
                return

            changes = []
            
            # Mute/deaf changes
            if before.self_mute != after.self_mute:
                changes.append(f"Self-mute: {'🔴 On' if after.self_mute else '🟢 Off'}")
            if before.self_deaf != after.self_deaf:
                changes.append(f"Self-deaf: {'🔴 On' if after.self_deaf else '🟢 Off'}")
            if before.mute != after.mute:
                changes.append(f"Server-mute: {'🔴 On' if after.mute else '🟢 Off'}")
            if before.deaf != after.deaf:
                changes.append(f"Server-deaf: {'🔴 On' if after.deaf else '🟢 Off'}")
            if before.self_stream != after.self_stream:
                changes.append(f"Streaming: {'🔴 On' if after.self_stream else '🟢 Off'}")
            if before.self_video != after.self_video:
                changes.append(f"Video: {'🔴 On' if after.self_video else '🟢 Off'}")
            
            # Only log if there are changes
            if changes:
                embed = discord.Embed(
                    title="🎚️ Voice State Update",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now()
                )
                
                embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
                embed.add_field(name="Channel", value=after.channel.mention if after.channel else "None", inline=False)
                embed.add_field(name="Changes", value="\n".join(changes), inline=False)
                
                await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VoiceStateLogger(bot))