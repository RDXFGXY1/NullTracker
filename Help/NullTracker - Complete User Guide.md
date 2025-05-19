# NullTracker - Complete User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Setup Commands](#setup-commands)
3. [Monitoring & Logging](#monitoring--logging)
4. [FAQ](#faq)


## Introduction

NullTracker is an advanced logging bot for Discord servers, designed to monitor and record server activities in real-time. It is modular, configurable, and easy to integrate into any Discord server that values organization, security, and insight.

## Setup Commands

NullTracker uses a hybrid command system, meaning it supports both traditional text commands and new slash (/) commands. All setup commands start with `@setlogchannel` (or your configured prefix) or `/setlogchannel`.

### Setting Up Log Channels

#### Message Logs

```
@setlogchannel messages [log_type]
```

Available message log types:
- `content_modifications` - Content modifications
- `pinned_messages` - Pinned messages
- `bulk_deletions` - Bulk deletions
- `reaction_changes` - Reaction changes

#### Voice Logs

```
@setlogchannel voice [voice_log_type]
```

Available voice log types:
- `connections` - Connections
- `state_changes` - State changes

#### Member Logs

```
@setlogchannel members [member_log_type]
```

Available member log types:
- `join_leave` - Join/Leave
- `bans_kicks` - Bans/Kicks
- `timeouts` - Timeouts
- `profile_changes` - Profile changes
- `role_updates` - Role updates

#### Role Logs

```
@setlogchannel roles [role_log_type]
```

Available role log types:
- `created` - Created roles
- `deleted` - Deleted roles
- `updated` - Updated roles

#### Server Logs

```
@setlogchannel server [server_log_type]
```

Available server log types:
- `appearance` - Appearance
- `community_updates` - Community updates
- `safety_settings` - Safety settings

#### Moderator Logs

```
@setlogchannel moderators [mod_log_type]
```

Available moderator log types:
- `warnings` - Warnings
- `automated_actions` - Automated actions
- `purges` - Purges

#### Channel Logs

```
@setlogchannel channels [channel_log_type]
```

Available channel log types:
- `lifecycle` - Lifecycle
- `permissions` - Permissions
- `slowmode` - Slowmode

#### Integration Logs

```
@setlogchannel integration [integration_logs_type]
```

Available integration log types:
- `webhooks` - Webhooks
- `bot_management` - Bot management

#### Emoji Logs

```
@setlogchannel emojis [emoji_log_type]
```

## Monitoring & Logging

NullTracker primarily functions as an automatic monitoring system. Once you've set up the log channels, it will automatically start monitoring and logging relevant events. No additional commands are required to start monitoring.

### Key Monitoring Features

#### Member Monitoring
- Track when members join and leave
- Log bans, unbans, and kicks
- Monitor nickname and profile changes

#### Role Monitoring
- Log role creations, deletions, and updates
- Track role permission changes
- Monitor role assignments to members

#### Voice Channel Monitoring
- Log voice channel connections
- Log voice channel disconnections
- Monitor user movements between channels
- Track voice state changes (mute/unmute, deafen/undeafen)

#### Channel Monitoring
- Log channel creation, deletion, and renaming
- Monitor channel permission updates
- Track slowmode changes

## FAQ

### How can I change the command prefix?
You can't change the command prefix. The prefix is set during setup and cannot be changed.

### Can I use one channel for all logs?
Yes, you can set the same channel for all log types. However, for better organization, we recommend using separate channels for different log types.


---

For more help or to report issues, please visit the [GitHub repository](https://github.com/RDXFGXY1/NullTracker) or join the NullStudio Discord server for support and updates.
