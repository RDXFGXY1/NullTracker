import discord
from discord.ext import commands
import json
import datetime
from typing import Optional


class MemberUpdateLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int, log_type: str) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["member_logs"][log_type]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        profile_changes = []
        role_changes = []
        
        # Nickname change
        if before.nick != after.nick:
            profile_changes.append(("Nickname", before.nick or "None", after.nick or "None"))
        
        # Role changes
        if before.roles != after.roles:
            added = [r.mention for r in after.roles if r not in before.roles]
            removed = [r.mention for r in before.roles if r not in after.roles]
            
            if added:
                role_changes.append(("Roles Added", "", ", ".join(added)))
            if removed:
                role_changes.append(("Roles Removed", "", ", ".join(removed)))
        
        # Handle profile changes
        if profile_changes:
            log_channel = await self.get_log_channel(after.guild.id, "profile_changes")
            if log_channel:
                embed = discord.Embed(
                    title="👤 Profile Updated",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now(datetime.UTC)
                )
                
                embed.set_author(name=f"{after} (ID: {after.id})", icon_url=after.display_avatar.url)
                
                for change in profile_changes:
                    embed.add_field(name=change[0], value=f"{change[1]} → {change[2]}", inline=False)

                await log_channel.send(embed=embed)

        # Handle role changes
        if role_changes:
            log_channel = await self.get_log_channel(after.guild.id, "role_updates")
            if log_channel:
                embed = discord.Embed(
                    title="🔄 Role Updated",
                    color=discord.Color.yellow(),
                    timestamp=datetime.datetime.now(datetime.UTC)
                )
                
                embed.set_author(name=f"{after} (ID: {after.id})", icon_url=after.display_avatar.url)
                
                for change in role_changes:
                    embed.add_field(name=change[0], value=change[2], inline=False)

                await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberUpdateLogger(bot))