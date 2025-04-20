# Null-Tracker

**Null-Tracker** is an advanced logging bot for Discord servers, designed to monitor and record server activities in real-time. It is modular, configurable, and easy to integrate into any Discord server that values organization, security, and insight.

## Features

Null-Tracker includes a comprehensive set of logging capabilities across various domains:

### ✅ Member Logs
- Track when members join, leave, are banned, unbanned, kicked, or updated.
- Fully modularized via `members_log` Cogs.

### ✅ Role Logs
- Logs role creations, deletions, and changes.

### ✅ Voice Logs
- Track voice channel events: connects, disconnects, moves, and state updates.

### ✅ Channel Logs
- Monitor creation, deletion, renaming, permission updates, and slowmode changes.

### ✅ Setup System
- Preconfigured setup group for quickly initializing logging channels, roles, emojis, integrations, and permissions.

### ✅ Premium Logs
- Includes support for extended logging and premium feature toggles.

## Folder Structure

```
null_tracker/
├── log_bot/
│   ├── cogs/
│   │   ├── members_log/
│   │   ├── role_logs/
│   │   ├── voice_logs/
│   │   ├── channels_log/
│   │   └── z_setup/
│   ├── config/
│   │   ├── main_config.json
│   │   └── config.json
│   ├── .env
│   ├── LICENSE.txt
│   ├── setup.py
│   └── requirements.txt
└── ...
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/null-tracker.git
   cd null-tracker/log_bot
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   - Create a `.env` file based on the provided template.
   - Edit `config/config.json` and `config/main_config.json` to fit your server's needs.

4. Run the bot:
   ```bash
   python setup.py
   ```

## Requirements

- Python 3.10 or later
- `discord.py` (or its maintained fork like `py-cord`)
- A bot token and a Discord application
- Basic understanding of Discord's permissions and events

## License

This project is licensed under the terms of the `LICENSE.txt` file.

## Contribution

Feel free to fork the repository and submit pull requests. Suggestions, feature requests, and bug reports are always welcome.

---

If you’re using this bot in production, consider joining the [Null-Studio Discord Server](https://discord.gg/YOUR_INVITE) for support and updates.
```
