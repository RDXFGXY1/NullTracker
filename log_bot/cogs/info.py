import discord
from discord.ext import commands
import json
from typing import Dict, Optional

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_config(self, guild_id: int) -> Optional[Dict]:
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                return json.load(f)
        except:
            return None

    @commands.command(aliases=['logsetup', 'logginginfo'])
    @commands.guild_only()
    async def info(self, ctx):
        """Check this server's logging configuration"""
        config = await self.get_config(ctx.guild.id)
        if not config:
            return await ctx.send("❌ No logging configuration found for this server.")

        embed = discord.Embed(
            title=f"📊 Logging Setup: {config['guild_name']}",
            color=0x2b2d31
        )
        embed.set_footer(text=f"Server Owner: {config['guild_owner']}")

        # Message Logging
        msg_fields = [
            ("✏️ Edits/Deletes", config["message_logs"]["content_modifications"]["channel_id"]),
            ("📌 Pins", config["message_logs"]["pinned_messages"]["channel_id"]),
            ("🧹 Bulk Deletes", config["message_logs"]["bulk_deletions"]["channel_id"]),
            ("👍 Reactions", config["message_logs"]["reaction_changes"]["channel_id"])
        ]
        msg_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in msg_fields
        )
        embed.add_field(name="💬 Message Logging", value=msg_value, inline=False)

        # Voice Logging
        voice_fields = [
            ("🎤 Connections", config["voice_logs"]["connections"]["channel_id"]),
            ("🎛️ State Changes", config["voice_logs"]["state_changes"]["channel_id"])
        ]
        voice_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in voice_fields
        )
        embed.add_field(name="🔊 Voice Logging", value=voice_value, inline=False)

        # Member Logging
        member_fields = [
            ("🔄 Joins/Leaves", config["member_logs"]["join_leave"]["channel_id"]),
            ("🔨 Bans/Kicks", config["member_logs"]["bans_kicks"]["channel_id"]),
            ("⏳ Timeouts", config["member_logs"]["timeouts"]["channel_id"]),
            ("👤 Profiles", config["member_logs"]["profile_changes"]["channel_id"]),
            ("🛡️ Roles", config["member_logs"]["role_updates"]["channel_id"])
        ]
        member_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in member_fields
        )
        embed.add_field(name="👥 Member Logging", value=member_value, inline=False)

        await ctx.send(embed=embed)

        # Second Embed (Continued)
        embed2 = discord.Embed(color=0x2b2d31)

        # Role Logging
        role_fields = [
            ("🆕 Created", config["role_logs"]["created"]["channel_id"]),
            ("❌ Deleted", config["role_logs"]["deleted"]["channel_id"]),
            ("✏️ Updated", config["role_logs"]["updated"]["channel_id"])
        ]
        role_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in role_fields
        )
        embed2.add_field(name="🎭 Role Logging", value=role_value, inline=False)

        # Server Logging
        server_fields = [
            ("🎨 Appearance", config["server_logs"]["appearance"]["channel_id"]),
            ("📢 Community", config["server_logs"]["community_updates"]["channel_id"]),
            ("🛡️ Safety", config["server_logs"]["safety_settings"]["channel_id"])
        ]
        server_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in server_fields
        )
        embed2.add_field(name="🏛️ Server Logging", value=server_value, inline=False)

        # Moderation Logging
        mod_fields = [
            ("⚠️ Warnings", config["moderation_logs"]["warnings"]["channel_id"]),
            ("🤖 Auto-Mod", config["moderation_logs"]["automated_actions"]["channel_id"]),
            ("🧹 Purges", config["moderation_logs"]["purges"]["channel_id"])
        ]
        mod_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in mod_fields
        )
        embed2.add_field(name="⚖️ Moderation Logging", value=mod_value, inline=False)

        await ctx.send(embed=embed2)

        # Third Embed (Continued)
        embed3 = discord.Embed(color=0x2b2d31)

        # Channel Logging
        channel_fields = [
            ("🔄 Lifecycle", config["channel_logs"]["lifecycle"]["channel_id"]),
            ("🔐 Permissions", config["channel_logs"]["permissions"]["channel_id"]),
            ("🐢 Slowmode", config["channel_logs"]["slowmode"]["channel_id"])
        ]
        channel_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in channel_fields
        )
        embed3.add_field(name="📁 Channel Logging", value=channel_value, inline=False)

        # Integration Logging
        integration_fields = [
            ("🪝 Webhooks", config["integration_logs"]["webhooks"]["channel_id"]),
            ("🤖 Bots", config["integration_logs"]["bot_management"]["channel_id"])
        ]
        integration_value = "\n".join(
            f"{name}: {f'<#{cid}>' if cid else '❌ Not configured'}"
            for name, cid in integration_fields
        )
        embed3.add_field(name="🔌 Integration Logging", value=integration_value, inline=False)

        await ctx.send(embed=embed3)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))