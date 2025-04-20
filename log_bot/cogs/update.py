import discord
from discord import app_commands
from discord.ext import commands
import json
from typing import Optional, List, Dict

class LogConfigUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_types = {
            # Message Logs
            "message_edits": ["message_logs", "content_modifications"],
            "message_pins": ["message_logs", "pinned_messages"],
            "bulk_deletes": ["message_logs", "bulk_deletions"],
            "reaction_changes": ["message_logs", "reaction_changes"],
            
            # Voice Logs
            "voice_connections": ["voice_logs", "connections"],
            "voice_state": ["voice_logs", "state_changes"],
            
            # Member Logs
            "joins_leaves": ["member_logs", "join_leave"],
            "bans_kicks": ["member_logs", "bans_kicks"],
            "timeouts": ["member_logs", "timeouts"],
            "profile_changes": ["member_logs", "profile_changes"],
            "role_updates": ["member_logs", "role_updates"],
            
            # Role Logs
            "role_created": ["role_logs", "created"],
            "role_deleted": ["role_logs", "deleted"],
            "role_updated": ["role_logs", "updated"],
            
            # Server Logs
            "server_appearance": ["server_logs", "appearance"],
            "community_updates": ["server_logs", "community_updates"],
            "safety_settings": ["server_logs", "safety_settings"],
            
            # Moderation Logs
            "warnings": ["moderation_logs", "warnings"],
            "auto_mod": ["moderation_logs", "automated_actions"],
            "purges": ["moderation_logs", "purges"],
            
            # Channel Logs
            "channel_lifecycle": ["channel_logs", "lifecycle"],
            "channel_perms": ["channel_logs", "permissions"],
            "slowmode": ["channel_logs", "slowmode"],
            
            # Integration Logs
            "webhooks": ["integration_logs", "webhooks"],
            "bot_management": ["integration_logs", "bot_management"]
        }

    async def update_config(self, guild_id: int, path: list, new_channel_id: int) -> bool:
        try:
            with open(f"servers/logs/{guild_id}.json", "r+") as f:
                config = json.load(f)
                current = config
                for key in path[:-1]:
                    current = current[key]
                current[path[-1]]["channel_id"] = new_channel_id
                
                f.seek(0)
                json.dump(config, f, indent=4)
                f.truncate()
                return True
        except Exception as e:
            print(f"Error updating config: {e}")
            return False

    @app_commands.command(name="update_log", description="Update a logging channel configuration")
    @app_commands.describe(
        log_type="Type of logs to configure",
        channel="Channel where logs will be sent"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def update_log(self, interaction: discord.Interaction, 
                    log_type: str, channel: discord.TextChannel):
        """Update logging channel with slash command"""
        log_type = log_type.lower()
        if log_type not in self.log_types:
            valid_types = "\n".join([f"- `{name}`" for name in self.log_types.keys()])
            embed = discord.Embed(
                title="❌ Invalid Log Type",
                description=f"Available types:\n{valid_types}",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        success = await self.update_config(interaction.guild_id, self.log_types[log_type], channel.id)
        if success:
            embed = discord.Embed(
                title="✅ Log Channel Updated",
                description=f"Set {channel.mention} for `{log_type}` logging",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Update Failed",
                description="Could not update configuration file",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)

    @update_log.autocomplete("log_type")
    async def log_type_autocomplete(self, 
                                  interaction: discord.Interaction,
                                  current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=name, value=name)
            for name in self.log_types.keys()
            if current.lower() in name.lower()
        ][:25]

    @update_log.error
    async def update_log_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                title="⛔ Permission Denied",
                description="You need `Manage Server` permissions to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.BadArgument):
            embed = discord.Embed(
                title="❌ Invalid Channel",
                description="Please select a valid text channel",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(LogConfigUpdater(bot))