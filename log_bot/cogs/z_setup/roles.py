import discord
from discord.ext import commands
import json


class SetupRoleLogChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def setup_role_logs(self, ctx, log_type: str):
        """Setup a channel for role logs (created/deleted/updated)"""
        if not isinstance(ctx.channel, discord.TextChannel):
            embed = discord.Embed(
                description="❌ This is not a text channel.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        valid_log_types = ["created", "deleted", "updated"]
        log_type = log_type.lower()
        
        if log_type not in valid_log_types:
            embed = discord.Embed(
                description=f"❌ Invalid log type. Available types: {', '.join(valid_log_types)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            with open(f"servers/logs/{ctx.guild.id}.json", "r", encoding="utf-8") as f:
                guild_data = json.load(f)
                
                # Check if channel is already set for this log type
                if ctx.channel.id == guild_data["role_logs"][log_type]["channel_id"]:
                    embed = discord.Embed(
                        description=f"⚠️ This channel is already setup for role {log_type} logs.",
                        color=discord.Color.yellow()
                    )
                    await ctx.send(embed=embed)
                    return
                
                # Update the channel ID
                with open(f"servers/logs/{ctx.guild.id}.json", "w", encoding="utf-8") as f:
                    guild_data["role_logs"][log_type]["channel_id"] = ctx.channel.id
                    json.dump(guild_data, f, indent=4, ensure_ascii=False)
                    
                    embed = discord.Embed(
                        description=f"✅ Channel {ctx.channel.mention} has been set for role **{log_type}** logs.",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    
        except FileNotFoundError:
            embed = discord.Embed(
                description="❌ Server log file not found. Please initialize server logs first.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except json.JSONDecodeError:
            embed = discord.Embed(
                description="❌ Error reading server log file.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(
                description="❌ Invalid log type or corrupted log file structure.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(SetupRoleLogChannel(bot))