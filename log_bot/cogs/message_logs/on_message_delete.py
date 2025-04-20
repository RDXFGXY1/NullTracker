import discord
from discord.ext import commands
import json
import datetime
from typing import Dict, Optional

class DeletedMessagesLogger(commands.Cog):
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
            'timestamp': datetime.datetime.now().timestamp(),
            'attachments': [a.url for a in message.attachments]
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
        """Get deletion log channel with priority system"""
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                return (config["message_logs"]["content_modifications"]["channel_id"])
        except:
            return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Cache messages for potential deletion logging"""
        await self.cache_message(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Handle message deletion logging"""
        if not message.guild:
            return

        log_channel_id = await self.get_log_channel(message.guild.id)
        if not log_channel_id:
            return

        log_channel = message.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        # Get cached data or fallback
        cached = self.message_cache.get(message.guild.id, {}).pop(message.id, {})
        author = message.author or await self.get_user(cached.get('author', 0))
        
        embed = discord.Embed(
            title="🗑️ Message Deleted",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        
        if hasattr(author, 'display_avatar'):
            embed.set_author(
                name=f"{author} (ID: {author.id})",
                icon_url=author.display_avatar.url
            )
        else:
            embed.set_author(name=str(author))
            
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        
        if content := cached.get('content', message.content):
            embed.add_field(
                name="Content", 
                value=content[:1000] + ("..." if len(content) > 1000 else ""),
                inline=False
            )
            
        if attachments := cached.get('attachments', []):
            embed.add_field(
                name="Attachments",
                value="\n".join(f"[File {i+1}]({url})" for i, url in enumerate(attachments)),
                inline=False
            )
            
        await log_channel.send(embed=embed)

    async def get_user(self, user_id: int):
        """Fetch user with fallback"""
        try:
            return await self.bot.fetch_user(user_id)
        except:
            return f"Unknown User (ID: {user_id})"

async def setup(bot):
    await bot.add_cog(DeletedMessagesLogger(bot))