import discord
from discord.ext import commands
from discord import app_commands
import os
import json


class SetupMessageLogChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_message_log_channel(self, ctx, log_type: str):
        if not isinstance(ctx.channel, discord.TextChannel):
            embed = discord.Embed(
                description="❌ This is not a text channel.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        try:
            with open(f"servers/logs/{ctx.guild.id}.json", "r", encoding="utf-8") as f:
                guild_data = json.load(f)
                if ctx.channel.id == guild_data["message_logs"][log_type]["channel_id"]:
                    embed = discord.Embed(
                        description="⚠️ This channel is already setup for this log type.",
                        color=discord.Color.yellow()
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    with open(f"servers/logs/{ctx.guild.id}.json", "w", encoding="utf-8") as f:
                        guild_data["message_logs"][log_type]["channel_id"] = ctx.channel.id
                        json.dump(guild_data, f, indent=4, ensure_ascii=False)
                        embed = discord.Embed(
                            description=f"✅ Channel {ctx.channel.mention} has been set for **{log_type}** logs.",
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=embed)
                        return
        except FileNotFoundError:
            embed = discord.Embed(
                description="❌ Server log file not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        except json.JSONDecodeError:
            embed = discord.Embed(
                description="❌ Error reading server log file.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

            return
async def setup(bot):
    await bot.add_cog(SetupMessageLogChannel(bot))
