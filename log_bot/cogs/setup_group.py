import discord
from discord.ext import commands

class Setup(commands.GroupCog, group_name="setlogchannel"):
    def __init__(self, bot):
        self.bot = bot
        self.message_log_type = ["content_modifications", "pinned_messages", "bulk_deletions", "reaction_changes"]
        self.voice_log_type = ["connections", "state_changes"]
        self.member_log_type = ["join_leave", "bans_kicks", "timeouts", "profile_changes", "role_updates"]
        self.role_log_type = ["created", "deleted", "updated"]
        self.server_log_type = ["appearance", "community_updates", "safety_settings"]
        self.mod_log_type = ["warnings", "automated_actions", "purges"]
        self.channel_log_type = ["lifecycle", "permissions", "slowmode"]
        self.integration_logs_type = ["webhooks", "bot_management"]        

###########################
#      Setup Commands     #
###########################

    #! Setup Messages Log Channel Command
    @commands.hybrid_command(name="messages", help="Set a channel for message logs.")
    async def set_message_log_channel(self, ctx, log_type: str):
        """Set the channel for message logs."""
        # Check if the log_type is valid
        await self.bot.get_cog("SetupMessageLogChannel").set_message_log_channel(ctx, log_type)

    #? Auto completion for the log_type parameter
    @set_message_log_channel.autocomplete("log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.message_log_type if current.lower() in log_type.lower()
        ]        

    #! Setup Voice Log Channel Command
    @commands.hybrid_command(name="voice", help="Setup a voice channel for voice logs.")
    async def set_voice_log_channel(self, ctx, voice_log_type: str):
        """Set the channel for voice logs."""
        await self.bot.get_cog("SetupVoiceLogChannel").set_voice_log_channel(ctx, voice_log_type)
        

    #! Setup Memebers Log Channel Command
    @commands.hybrid_command(name="members", help="Setup a channel for member logs.")
    async def set_member_log_channel(self, ctx, memeber_log_type: str):
        """ Set the channel for member logs. """
        await self.bot.get_cog("SetupMemberLogChannel").setup_member_logs(ctx, memeber_log_type)

    @commands.hybrid_command(name="roles", help="Setup a channel for role logs.")
    async def set_role_log_channel(self, ctx, role_log_type: str):
        """ Set the channel for role logs. """
        await self.bot.get_cog("SetupRoleLogChannel").setup_role_logs(ctx, role_log_type)

    @commands.hybrid_command(name="integration", help="Setup a channel for permission logs.")
    async def set_permission_log_channel(self, ctx, integration_logs_type: str):
        """ Set the channel for permission logs. """
        await self.bot.get_cog("SetupIntegrationLogs").setup_integration_logs(ctx, integration_logs_type)

    @commands.hybrid_command(name="moderators", help="Setup a channel for moderator logs.")
    async def set_mod_log_channel(self, ctx, mod_log_type: str):
        """ Set the channel for moderator logs. """
        await self.bot.get_cog("SetupModeratorLogs").setup_mod_logs(ctx, mod_log_type)

    @commands.hybrid_command(name="emojis", help="Setup a channel for emoji/sticker logs.")
    async def set_emoji_log_channel(self, ctx, emoji_log_type: str):
        """ Set the channel for emoji/sticker logs. """
        await self.bot.get_cog("SetupEmojiLogs").setup_emoji_logs(ctx, emoji_log_type)
        
    @commands.hybrid_command(name="server", help="Setup a channel for server logs.")
    async def set_server_log_channel(self, ctx, server_log_type: str):
        """ Set the channel for server logs. """
        await self.bot.get_cog("SetupServerLogs").setup_server_logs(ctx, server_log_type)

    @commands.hybrid_command(name="channels", help="Setup a channel for channel logs.")
    async def set_channel_log_channel(self, ctx, channel_log_type: str):
        """ Set the channel for channel logs. """
        await self.bot.get_cog("SetupChannelLogs").setup_channel_logs(ctx, channel_log_type)

#! ======================Auto Complet==============================

    #? Auto completion for the voice_log_type parameter
    @set_voice_log_channel.autocomplete("voice_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.voice_log_type if current.lower() in log_type.lower()
        ]

    #? Auto completion for the member_log_type
    @set_member_log_channel.autocomplete("memeber_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.member_log_type if current.lower() in log_type.lower()
        ]
    
    #? Auto completion for the role_log_type
    @set_role_log_channel.autocomplete("role_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.role_log_type if current.lower() in log_type.lower()
        ]
    
    #? Auto completion for the integration_logs_type
    @set_permission_log_channel.autocomplete("integration_logs_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.integration_logs_type if current.lower() in log_type.lower()
        ]
    
    #? Auto completion for the mod_log_type
    @set_mod_log_channel.autocomplete("mod_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.mod_log_type if current.lower() in log_type.lower()
        ]
    
    #? Auto completion for the emoji_log_type
    @set_emoji_log_channel.autocomplete("emoji_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.emoji_log_type if current.lower() in log_type.lower()
        ]
    
    #? Auto completion for the server_log_type
    @set_server_log_channel.autocomplete("server_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.server_log_type if current.lower() in log_type.lower()
        ]

    #? Auto completion for the channel_log_type
    @set_channel_log_channel.autocomplete("channel_log_type")
    async def log_type_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name=log_type, value=log_type)
            for log_type in self.channel_log_type if current.lower() in log_type.lower()
        ]
        
async def setup(bot):
    await bot.add_cog(Setup(bot))