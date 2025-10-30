# 🚀 Telegram File Manager Bot

A powerful and lightning-fast Telegram bot that automatically forwards files to a channel without downloading. Files are stored with unique 9-digit numeric IDs for instant retrieval.

## ✨ Features

- 🌍 **Multi-language Support**: English, Hebrew, Spanish, Korean, French, Chinese
- ⚡ **Lightning Fast**: No file downloading - direct forwarding only
- 🔐 **Secure**: All files stored in your Telegram channel
- 🆔 **Unique IDs**: Every file gets a unique 9-digit numeric ID
- 📱 **Simple Commands**: `/file <id>` to retrieve any file instantly
- 🎨 **Modern UI**: Smooth language selection and beautiful welcome messages
- 💾 **Persistent Storage**: MongoDB ensures data survives restarts
- 🚀 **Heroku Optimized**: Configured for Standard-2X dynos on heroku-24 stack

## 📋 Requirements

- Python 3.12.7
- MongoDB database
- Telegram Bot Token
- Telegram Channel (Public or Private)

## 🛠️ Setup Instructions

### 1. Create Telegram Bot

1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy your bot token

### 2. Create Channel

1. Create a new Telegram channel (public or private)
2. Add your bot as an administrator with full permissions
3. Get channel identifier:
   - **For Public Channel**: Use username like `@yourchannel`
   - **For Private Channel**: Forward any message to [@userinfobot](https://t.me/userinfobot) and copy ID (starts with -100)

### 3. Setup MongoDB

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist IP: `0.0.0.0/0` (allow from anywhere)
5. Get your connection string

### 4. Deploy to Heroku

#### Option A: One-Click Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

1. Click the deploy button above
2. Fill in the environment variables:
   - `BOT_TOKEN`: Your bot token from BotFather
   - `MONGO_URI`: Your MongoDB connection string
   - `PRIVATE_CHANNEL_ID`: Channel username (@yourchannel) OR channel ID (-1001234567890)
3. Click "Deploy app"
4. App will automatically deploy on Standard-2X dyno with stack-24

#### Option B: Manual Deploy

```bash
git clone https://github.com/rinlte/tb.git
cd tb
heroku create your-app-name
heroku stack:set heroku-24
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set MONGO_URI=your_mongodb_uri
heroku config:set PRIVATE_CHANNEL_ID=@yourchannel
git push heroku main
heroku ps:scale worker=1
heroku ps:type worker=standard-2x
```

## 📱 Bot Commands

- `/start` - Start the bot and select language
- `/file <id>` - Retrieve file by unique ID

## 🎯 Usage

1. Start the bot: `/start`
2. Choose your language from the button menu
3. Send any file (document, photo, video, audio, etc.)
4. Bot forwards it to your channel and gives you a unique 9-digit ID
5. Retrieve anytime with: `/file 123456789`

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Your Telegram bot token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `MONGO_URI` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| `PRIVATE_CHANNEL_ID` | Channel username or ID | `@yourchannel` or `-1001234567890` |

## 📊 Supported File Types

- 📄 Documents
- 🖼️ Photos
- 🎥 Videos
- 🎵 Audio
- 🎤 Voice Messages
- 🎬 Video Notes
- 🎞️ Animations/GIFs
- 🎨 Stickers

## 🌐 Supported Languages

- 🇬🇧 English
- 🇮🇱 Hebrew (עברית)
- 🇪🇸 Spanish (Español)
- 🇰🇷 Korean (한국어)
- 🇫🇷 French (Français)
- 🇨🇳 Chinese (中文)

## 💡 How It Works

1. User sends a file to the bot
2. Bot forwards the file to your channel (no download)
3. File metadata and channel message ID saved to MongoDB
4. Unique 9-digit ID generated and returned to user
5. When user requests file with `/file <id>`, bot forwards from channel

## 🚀 Performance

- **Stack**: heroku-24 (latest)
- **Dyno Type**: Standard-2X
- **No File Downloads**: Uses Telegram's forward API
- **Fast Retrieval**: Direct forwarding from channel
- **Scalable**: Handles massive concurrent users

## 📝 License

MIT License - feel free to use and modify

## 🤝 Support

For issues or questions, open an issue on [GitHub](https://github.com/rinlte/tb/issues)

## ⚠️ Important Notes

- Bot must be admin in the channel
- Channel can be public (@username) or private (ID)
- MongoDB connection string must allow connections from anywhere
- Keep your bot token and MongoDB URI secret
- Standard-2X dyno provides optimal performance

---

Made with ❤️ for efficient file management
