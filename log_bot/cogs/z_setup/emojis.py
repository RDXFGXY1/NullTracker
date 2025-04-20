import discord
from discord.ext import commands
import json

class SetupEmojiLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def setup_emoji_logs(self, ctx, log_type: str):
        """Set up emoji/sticker tracking channel
        Available types: created, deleted, updated"""
        
        if not isinstance(ctx.channel, discord.TextChannel):
            embed = discord.Embed(
                description="❌ This command can only be used in text channels.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Map log types to friendly names
        log_types = {
            "created": "emoji/sticker creations",
            "deleted": "emoji/sticker deletions",
            "updated": "emoji/sticker updates"
        }

        log_type = log_type.lower()

        if log_type not in log_types:
            embed = discord.Embed(
                description=f"❌ Invalid log type. Available types: {', '.join(log_types.keys())}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            # Load existing config
            with open(f"servers/logs/{ctx.guild.id}.json", "r", encoding="utf-8") as f:
                guild_data = json.load(f)

            # Check if channel already set
            if guild_data["emoji_logs"][log_type]["channel_id"] == ctx.channel.id:
                embed = discord.Embed(
                    description=f"⚠️ This channel already tracks {log_types[log_type]}.",
                    color=discord.Color.yellow()
                )
                await ctx.send(embed=embed)
                return

            # Update configuration
            guild_data["emoji_logs"][log_type]["channel_id"] = ctx.channel.id
            
            with open(f"servers/logs/{ctx.guild.id}.json", "w", encoding="utf-8") as f:
                json.dump(guild_data, f, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                description=f"✅ {ctx.channel.mention} will now log {log_types[log_type]}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except FileNotFoundError:
            embed = discord.Embed(
                description="❌ Server logging not configured. Please run initial setup first.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except json.JSONDecodeError:
            embed = discord.Embed(
                description="❌ Configuration file corrupted. Please reset logging config.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Unexpected error: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    
async def setup(bot):
    await bot.add_cog(SetupEmojiLogs(bot))