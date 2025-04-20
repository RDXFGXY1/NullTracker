
# Null-Tracker

Null-Tracker is a powerful and modular Discord bot designed to monitor, log, and manage various server activities in real-time. It is built with scalability and customization in mind, making it ideal for both small communities and large servers.

> 📅 Version: 2.0  
> 📌 Author: [Null-Studio](https://discord.gg/nullstudio)  
> 🧠 Language: Python 3.12  
> 📁 Modular Structure | 💾 Persistent Logs | 💼 Premium Log Support

---

## 🔍 Features

### ✅ Member Activity Logging
- Member joins, leaves, bans, unbans, updates, and kicks.
- Stored in `cogs/members_log/`.

### 🎙️ Voice Channel Logging
- Tracks user connections, disconnections, movements, and status updates in voice channels.
- Stored in `cogs/voice_logs/`.

### 🛠️ Role Management Logging
- Monitors role creations, deletions, and edits.
- Stored in `cogs/role_logs/`.

### 🔊 Channel Logs
- Tracks changes in channel lifecycle, slowmode, and permissions.
- Stored in `cogs/channels_log/`.

### 🚀 Server Setup Tools
- Powerful setup commands for roles, emojis, permissions, integration, and more.
- Stored in `cogs/z_setup/`.

### 💎 Premium Logging
- Advanced logging tools for premium users.
- Found in `PremiumLogs.py`.

---

## ⚙️ Configuration

All configuration files are stored under the `config/` directory:
- `main_config.json`: Main settings for the bot.
- `config.json`: Additional config entries.
- `.env`: Environment variables for tokens and secrets.

---

## 🧩 Installation

> Requires Python 3.12+

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/null-tracker.git
cd null-tracker/log_bot
```

2. Set up the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Add your `.env` file and configure your `main_config.json`.

5. Run the bot:
```bash
python3 setup.py
```

---

## 📜 License

This project is licensed under the terms of the `LICENSE.txt` file.

---

## 🤝 Contributing

Contributions, suggestions, and issues are welcome! Feel free to fork and submit pull requests.

---

## 📞 Support

For support or business inquiries, join our [Discord server](https://discord.gg/nullstudio) or contact the team at `Null-Studio`.

---

> Built with ❤️ by Null-Studio
```

إذا بغيت أضيف صورة، شارة GitHub، رابط مباشر للـ invite، أو توثيق للأوامر، قول لي ونكمل عليه.
