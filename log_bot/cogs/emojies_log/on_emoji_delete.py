import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class EmojiDeleteLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild_id: int) -> Optional[discord.TextChannel]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["server_logs"]["community_updates"]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: list, after: list):
        # Find deleted emojis
        deleted_emojis = [e for e in before if e not in after]
        
        for emoji in deleted_emojis:
            log_channel = await self.get_log_channel(guild.id)
            if not log_channel:
                continue

            embed = discord.Embed(
                title="❌ Emoji Deleted",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            
            embed.add_field(name="Name", value=f":{emoji.name}:", inline=True)
            embed.add_field(name="ID", value=emoji.id, inline=True)
            embed.add_field(name="Animated", value="Yes" if emoji.animated else "No", inline=True)
            
            # Check who deleted it
            if guild.me.guild_permissions.view_audit_log:
                async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.emoji_delete):
                    if entry.target.id == emoji.id:
                        embed.add_field(name="Deleted By", value=entry.user.mention, inline=False)
                        if entry.reason:
                            embed.add_field(name="Reason", value=entry.reason, inline=False)
                        break
            
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EmojiDeleteLogger(bot))