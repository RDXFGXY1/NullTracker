import discord
from discord.ext import commands
import os
import json
import asyncio

class BotJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):  # غيرت الحدث لـ on_guild_join عشان ده الصح لما البوت يدخل سيرفر
        # إرسال رسالة ترحيب لصاحب السيرفر
        owner = await self.bot.fetch_user(guild.owner_id)
        await owner.send(f"Thanks for inviting me to {guild.name}! I'm here to help you manage your server.\n Please Wait im setting up my self!")

        # التأكد من إن مجلد servers/logs & backup موجود
        os.makedirs("servers/logs", exist_ok=True)
        os.makedirs("servers/backup", exist_ok=True)

        # إنشاء ملف JSON باسم الـ guild id & backup
        file_path = f"servers/logs/{guild.id}.json"
        backup_path = f"servers/backup/{guild.id}.txt"
        
        # الستراكتشر اللي عايزها
        guild_data = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "guild_owner": guild.owner.name,
            
            # Message Tracking
            "message_logs": {
                "content_modifications": {  # Combined deleted/edited
                    "channel_id": None  
                },
                "pinned_messages": {
                    "channel_id": None
                },
                "bulk_deletions": {  # New
                    "channel_id": None
                },
                "reaction_changes": {  # New
                    "channel_id": None
                }
            },
            
            # Voice Activity
            "voice_logs": {
                "connections": {  # Combined joined/left/switched
                    "channel_id": None
                },
                "state_changes": {  # New (mute/deafen/stream)
                    "channel_id": None
                }
            },
            
            # Member Activity
            "member_logs": {
                "join_leave": {  # Combined
                    "channel_id": None
                },
                "bans_kicks": {  # Combined
                    "channel_id": None
                },
                "timeouts": {  # New
                    "channel_id": None
                },
                "profile_changes": {  # New (nicknames/avatars)
                    "channel_id": None
                },
                "role_updates": {  # New (role additions/removals)
                    "channel_id": None
                }
            },
            
            # Role Management
            "role_logs": {
                "created": {
                    "channel_id": None
                },
                "deleted": {
                    "channel_id": None
                },
                "updated": {
                    "channel_id": None
                }
            },
            
            # Server Changes
            "server_logs": {
                "appearance": {  # Name/icon
                    "channel_id": None
                },
                "community_updates": {  # New (rules/guidelines)
                    "channel_id": None
                },
                "safety_settings": {  # New (verification levels)
                    "channel_id": None
                }
            },
            
            # Moderation Actions
            "moderation_logs": {  # New category
                "warnings": {
                    "channel_id": None
                },
                "automated_actions": {  # Anti-raid/spam
                    "channel_id": None
                },
                "purges": {  # Purge commands
                    "channel_id": None
                }
            },
            
            # Channel Management
            "channel_logs": {  # New category
                "lifecycle": {  # Created/deleted
                    "channel_id": None
                },
                "permissions": {
                    "channel_id": None
                },
                "slowmode": {  # New
                    "channel_id": None
                }
            },
            
            # Integration Logs
            "integration_logs": {  # New category
                "webhooks": {
                    "channel_id": None
                },
                "bot_management": {  # Bot add/remove
                    "channel_id": None
                }
            }
        }

        backup_data = f"Server {guild.name} Backup\n\n"

        # كتابة الستراكتشر في الملف
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(guild_data, f, indent=4, ensure_ascii=False)

        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(backup_data)
        

        #wait 2 sec
        await asyncio.sleep(2)
        await owner.send(" Well im done! you can use me as you like \n for more infromation about me or any update join my server !")

        # إرسال رسالة ترحيب في السيستم تشانل لو موجودة
        if guild.system_channel:
            welcome_message = (
                "Welcome to the server! I'm here to help you manage your server. "
                "You can use the following commands to get started:\n\n"
                "`/setlogchannel <log_type>` - Set the channel for logging deleted and edited messages.\n"
                "For more inforamtion type `/help`"
            )
            await guild.system_channel.send(welcome_message)


async def setup(bot):
    await bot.add_cog(BotJoin(bot))