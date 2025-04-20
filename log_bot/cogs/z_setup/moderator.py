import discord
from discord.ext import commands
import json

class SetupModeratorLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def setup_mod_logs(self, ctx, log_type: str):
        """Set up moderator action logs channel
        Available types: ban_added, ban_removed, mute_added, mute_removed"""
        
        if not isinstance(ctx.channel, discord.TextChannel):
            embed = discord.Embed(
                description="❌ This command can only be used in text channels.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        valid_log_types = {
            "warnings": "Warnings",
            "automated_actions": "Automated Actions",
            "purges": "Message Purges"        }

        log_type = log_type.lower()

        if log_type not in valid_log_types:
            embed = discord.Embed(
                description=f"❌ Invalid log type. Available types: {', '.join(valid_log_types.keys())}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            with open(f"servers/logs/{ctx.guild.id}.json", "r", encoding="utf-8") as f:
                guild_data = json.load(f)

            # Check if already set to this channel
            if guild_data["moderation_logs"][log_type]["channel_id"] == ctx.channel.id:
                embed = discord.Embed(
                    description=f"⚠️ This channel is already set for {valid_log_types[log_type]} logs.",
                    color=discord.Color.yellow()
                )
                await ctx.send(embed=embed)
                return

            # Update config
            guild_data["moderation_logs"][log_type]["channel_id"] = ctx.channel.id
            
            with open(f"servers/logs/{ctx.guild.id}.json", "w", encoding="utf-8") as f:
                json.dump(guild_data, f, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                description=f"✅ {ctx.channel.mention} is now set for {valid_log_types[log_type]} logs.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except FileNotFoundError:
            embed = discord.Embed(
                description="❌ Server logging not configured. Please run initial setup first.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ An error occurred: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SetupModeratorLogs(bot))