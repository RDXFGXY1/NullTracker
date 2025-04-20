import discord
from discord.ext import commands
import json
import datetime
from typing import Optional

class EmojiUpdateLogger(commands.Cog):
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
        # Find updated emojis
        updated_emojis = []
        for b_emoji in before:
            for a_emoji in after:
                if b_emoji.id == a_emoji.id and b_emoji.name != a_emoji.name:
                    updated_emojis.append((b_emoji, a_emoji))
        
        for before_emoji, after_emoji in updated_emojis:
            log_channel = await self.get_log_channel(guild.id)
            if not log_channel:
                continue

            embed = discord.Embed(
                title="✏️ Emoji Updated",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            
            embed.set_thumbnail(url=after_emoji.url)
            embed.add_field(name="Before", value=f":{before_emoji.name}:", inline=True)
            embed.add_field(name="After", value=f":{after_emoji.name}:", inline=True)
            embed.add_field(name="ID", value=after_emoji.id, inline=True)
            
            # Check who updated it
            if guild.me.guild_permissions.view_audit_log:
                async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.emoji_update):
                    if entry.target.id == after_emoji.id:
                        embed.add_field(name="Updated By", value=entry.user.mention, inline=False)
                        if entry.reason:
                            embed.add_field(name="Reason", value=entry.reason, inline=False)
                        break
            
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EmojiUpdateLogger(bot))