import discord
from discord.ext import commands
import json
import datetime
from typing import Dict, List, Optional, Tuple

class RoleLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_cache: Dict[int, Dict[int, dict]] = {}  # {guild_id: {role_id: role_data}}

    async def cache_roles(self, guild: discord.Guild):
        """Cache all existing roles with their properties"""
        self.role_cache[guild.id] = {}
        for role in guild.roles:
            self.cache_role_data(role)

    def cache_role_data(self, role: discord.Role):
        """Store relevant role data in cache"""
        self.role_cache[role.guild.id][role.id] = {
            'name': role.name,
            'color': str(role.color),
            'hoist': role.hoist,
            'position': role.position,
            'mentionable': role.mentionable,
            'permissions': dict(role.permissions)
        }

    async def get_log_channel(self, guild_id: int, log_type: str) -> Optional[discord.TextChannel]:
        """Get the appropriate log channel for role events"""
        try:
            with open(f"servers/logs/{guild_id}.json", "r") as f:
                config = json.load(f)
                if channel_id := config["role_logs"][log_type]["channel_id"]:
                    return self.bot.get_channel(channel_id)
        except:
            return None

    @commands.Cog.listener()
    async def on_ready(self):
        """Cache all roles when bot starts"""
        for guild in self.bot.guilds:
            await self.cache_roles(guild)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        """Track new role creation"""
        self.cache_role_data(role)
        await self.log_role_change(role.guild, "created", role)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """Track role deletion using cached data"""
        cached_data = self.role_cache.get(role.guild.id, {}).pop(role.id, None)
        if cached_data:
            await self.log_role_change(role.guild, "deleted", role, cached_data)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        """Track all role updates with detailed changes"""
        changes = await self.detect_role_changes(before, after)
        if changes:
            self.cache_role_data(after)
            await self.log_role_change(after.guild, "updated", after, changes)

    async def detect_role_changes(self, before: discord.Role, after: discord.Role) -> List[Tuple[str, str, str]]:
        """Identify all changes between role versions"""
        changes = []
        
        if before.name != after.name:
            changes.append(("Name", before.name, after.name))
        if before.color != after.color:
            changes.append(("Color", str(before.color), str(after.color)))
        if before.hoist != after.hoist:
            changes.append(("Hoist", str(before.hoist), str(after.hoist)))
        if before.mentionable != after.mentionable:
            changes.append(("Mentionable", str(before.mentionable), str(after.mentionable)))
        if before.position != after.position:
            changes.append(("Position", str(before.position), str(after.position)))
        
        # Permission changes
        perm_changes = []
        for perm, value in after.permissions:
            if getattr(before.permissions, perm) != value:
                perm_changes.append(f"{perm}: {'✅' if value else '❌'}")
        if perm_changes:
            changes.append(("Permissions", "\n".join(perm_changes), ""))
        
        return changes

    async def log_role_change(self, guild: discord.Guild, action: str, role: discord.Role, 
                            extra_data=None, before_data=None):
        """Generate and send the appropriate log embed"""
        log_channel = await self.get_log_channel(guild.id, action)
        if not log_channel:
            return

        embed = discord.Embed(
            title={
                "created": "🆕 Role Created",
                "updated": "✏️ Role Updated", 
                "deleted": "❌ Role Deleted"
            }[action],
            color=role.color if action != "deleted" else discord.Color.red(),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(name="Role", value=f"{role.name} (ID: {role.id})", inline=False)
        
        if action == "created":
            embed.add_field(name="Color", value=str(role.color), inline=True)
            embed.add_field(name="Position", value=role.position, inline=True)
            embed.description = f"New role created with {len(role.permissions)} permissions"
        
        elif action == "updated" and extra_data:
            change_text = []
            for field, old_val, new_val in extra_data:
                if field == "Permissions":
                    change_text.append(f"**{field} Changes:**\n{old_val}")
                else:
                    change_text.append(f"**{field}:** {old_val} → {new_val}")
            embed.add_field(name="Changes", value="\n".join(change_text), inline=False)
        
        elif action == "deleted" and extra_data:  # extra_data is cached role data
            embed.add_field(name="Basic Info", 
                          value=f"Color: {extra_data['color']}\nPosition: {extra_data['position']}", 
                          inline=False)
            embed.add_field(name="Permissions", 
                          value=f"{len(extra_data['permissions'])} permissions set", 
                          inline=False)

        # Add audit log info
        audit_action = {
            "created": discord.AuditLogAction.role_create,
            "updated": discord.AuditLogAction.role_update,
            "deleted": discord.AuditLogAction.role_delete
        }[action]

        async for entry in guild.audit_logs(limit=5, action=audit_action):
            if entry.target.id == role.id:
                embed.add_field(name="Action By", value=entry.user.mention, inline=False)
                if entry.reason:
                    embed.add_field(name="Reason", value=entry.reason, inline=False)
                break

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        """Cache roles when guild becomes available"""
        await self.cache_roles(guild)

async def setup(bot):
    await bot.add_cog(RoleLogger(bot))