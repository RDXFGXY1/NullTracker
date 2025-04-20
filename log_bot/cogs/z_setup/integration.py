import discord
from discord.ext import commands
import json

class SetupIntegrationLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def setup_integration_logs(self, ctx, log_type: str):
        """Set up integration logs channel (webhooks or bot_management)"""
        
        if not isinstance(ctx.channel, discord.TextChannel):
            embed = discord.Embed(
                description="❌ This command can only be used in text channels.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        valid_log_types = ["webhooks", "bot_management"]
        log_type = log_type.lower()

        if log_type not in valid_log_types:
            embed = discord.Embed(
                description=f"❌ Invalid log type. Available types: {', '.join(valid_log_types)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            # Load existing config
            with open(f"servers/logs/{ctx.guild.id}.json", "r", encoding="utf-8") as f:
                guild_data = json.load(f)

            # Check if already set to this channel
            current_channel = guild_data["integration_logs"][log_type]["channel_id"]
            if current_channel == ctx.channel.id:
                embed = discord.Embed(
                    description=f"⚠️ This channel is already set for {log_type.replace('_', ' ')} logs.",
                    color=discord.Color.yellow()
                )
                await ctx.send(embed=embed)
                return

            # Update the config
            guild_data["integration_logs"][log_type]["channel_id"] = ctx.channel.id
            
            with open(f"servers/logs/{ctx.guild.id}.json", "w", encoding="utf-8") as f:
                json.dump(guild_data, f, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                description=f"✅ {ctx.channel.mention} is now set for {log_type.replace('_', ' ')} integration logs.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except FileNotFoundError:
            embed = discord.Embed(
                description="❌ Server logging not configured. Please set up logging first.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except json.JSONDecodeError:
            embed = discord.Embed(
                description="❌ Error reading server config. Please contact an admin.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(
                description="❌ Invalid configuration structure. Please reset logging config.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SetupIntegrationLogs(bot))