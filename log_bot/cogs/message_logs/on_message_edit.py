import discord
from discord.ext import commands
import json
import datetime
from typing import Dict, Optional

class EditedMessagesLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_cache = {}
        self.MAX_CACHE_SIZE = 500
        self.CACHE_TTL = 180  # 5 minutes

    async def cache_message(self, message: discord.Message):
        """Cache messages with size and time limits"""
        if not message.guild or message.author.bot:
            return

        guild_cache = self.message_cache.setdefault(message.guild.id, {})
        
        if len(guild_cache) >= self.MAX_CACHE_SIZE:
            self.clean_guild_cache(message.guild.id)
            
        guild_cache[message.id] = {
            'content': message.content,
            'author': message.author.id,
            'channel': message.channel.id,
            'timestamp': datetime.datetime.now().timestamp()
        }

    def clean_guild_cache(self, guild_id: int):
        """Remove oldest messages in a guild's cache"""
        current_time = datetime.datetime.now().timestamp()
        self.message_cache[guild_id] = {
            msg_id: msg_data 
            for msg_id, msg_data in self.message_cache.get(guild_id, {}).items()
            if current_time - msg_data['timestamp'] <= self.CACHE_TTL
        }[:self.MAX_CACHE_SIZE]

    async def get_log_channel(self, guild_id: int) -> Optional[int]:
        """Get edit log channel with priority system"""
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                return (config["message_logs"]["content_modifications"]["channel_id"])
        except:
            return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Cache messages for potential edit logging"""
        await self.cache_message(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Handle message edit logging"""
        if not after.guild or before.content == after.content:
            return

        log_channel_id = await self.get_log_channel(after.guild.id)
        if not log_channel_id:
            return

        log_channel = after.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        # Get original content from cache if available
        cached_content = self.message_cache.get(after.guild.id, {}).get(after.id, {}).get('content', before.content)

        embed = discord.Embed(
            title="✏️ Message Edited",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        
        embed.set_author(
            name=f"{after.author} (ID: {after.author.id})",
            icon_url=after.author.display_avatar.url
        )
        
        embed.add_field(name="Channel", value=after.channel.mention, inline=False)
        
        if after.jump_url:
            embed.add_field(name="Message Link", value=f"[Jump to Message]({after.jump_url})", inline=False)
            
        embed.add_field(
            name="Original Content",
            value=cached_content[:1000] + ("..." if len(cached_content) > 1000 else ""),
            inline=False
        )
        embed.add_field(
            name="Edited Content", 
            value=after.content[:1000] + ("..." if len(after.content) > 1000 else ""),
            inline=False
        )
        
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EditedMessagesLogger(bot))