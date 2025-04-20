import discord
from discord.ext import commands
import json
import datetime
from typing import Optional


class MemberRemoveLogger(commands.Cog):
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
    async def on_member_remove(self, member: discord.Member):
        log_channel = await self.get_logannel(member.guild.id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🔴 Member Left",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        
        embed.set_author(name=f"{member} (ID: {member.id})", icon_url=member.display_avatar.url)
        
        join_date = member.joined_at.strftime("%Y-%m-%d %H:%M") if member.joined_at else "Unknown"
        embed.add_field(name="Joined At", value=join_date, inline=True)
        
        duration = (datetime.datetime.now(datetime.timezone.utc) - member.joined_at).days if member.joined_at else "Unknown"
        embed.add_field(name="Duration", value=f"{duration} days", inline=True)
        
        roles = [r.mention for r in member.roles if not r.is_default()]
        if roles:
            embed.add_field(name="Roles", value=" ".join(roles[:5]) + ("..." if len(roles) > 5 else ""), inline=False)

        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberRemoveLogger(bot))