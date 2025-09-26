# Channel-Link-Bot

![Miku Nakano](https://images7.alphacoders.com/132/1323209.jpeg)

A Telegram bot to generate smart, temporary, and request-based invite links for your channels and groups.  
Helps you avoid problems and keep your communities safe.

---

## Features

- **Temporary Invite Links**: One-time, time-limited join links for channels/groups.
- **Request Links**: Join links that require admin approval.
- **Broadcast**: Send messages to all users.
- **Channel Management**: Register and remove channels/groups.
- **User Stats**: See how many users are using your bot.

---

## Getting Started

### 1. BotFather Commands

Set these commands in [BotFather](https://t.me/BotFather):

```
start - Start the bot or get a join link
setchannel - Register a channel/group
delchannel - Remove a channel/group
channelpost - Get join links for registered channels
reqpost - Get request join links for registered channels
broadcast - Broadcast a message to all users (admin only)
users - Show total users (admin only)
stats - Show bot stats (admin only)
```

---

## Configuration

Edit `config.py`:

```python
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
MONGO_URI = "your_mongodb_uri"
ADMINS = [123456789]  # Your Telegram user ID(s)
START_PIC = "https://images6.alphacoders.com/132/1323207.jpeg"  # Optional start image
LINK_PIC = "https://wallpaper.forfun.com/fetch/72/72d9ab0c3dfa4777c626ce6b8e056742.jpeg"  # Optional link image
```

---

## Usage

### Basic Commands

- `/start`  
  Start the bot. If used with a special link, generates a join link.

- `/setchannel @username` or `/setchannel -1001234567890`  
  Register a channel or group for invite link generation.

- `/delchannel @username` or `/delchannel -1001234567890`  
  Remove a registered channel or group.

- `/channelpost`  
  Get a list of join links for all registered channels.

- `/channelpost @username` or `/channelpost -1001234567890`  
  Get a join link for a specific channel/group.

- `/reqpost`  
  Get a list of request join links (admin approval required) for all registered channels.

- `/reqpost @username` or `/reqpost -1001234567890`  
  Get a request join link for a specific channel/group.

- `/broadcast`  
  (Admin only) Reply to a message to broadcast it to all users.

- `/users`  
  (Admin only) Show total users.

- `/stats`  
  (Admin only) Show bot and channel stats.

---

## How Invite Links Work

- **Normal Link**:  
  `/channelpost` gives you a deep link. When a user clicks it and starts the bot, they get a one-time, time-limited invite link.

- **Request Link**:  
  `/reqpost` gives you a deep link. When a user clicks it and starts the bot, they get a join request link (admin approval required).

- **All links are unique per user and expire after use or after 10 minutes.**

---

## Hosting

### Local Hosting

1. Clone the repo:
    ```bash
    git clone https://github.com/DARKXSIDE78/Channel-Link-Bot.git
    cd Channel-Link-Bot
    ```
2. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
3. Edit `config.py` with your credentials.
4. Run the bot:
    ```bash
    python3 bot.py
    ```

---

### Deploy on Railway

1. Fork this repo.
2. Go to [Railway](https://railway.app/) and create a new project from your GitHub repo.
3. Add your environment variables (`API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_URI`, etc.) in Railway's dashboard.
4. Deploy!

---

### Deploy on Koyeb

1. Fork this repo.
2. Go to [Koyeb](https://www.koyeb.com/) and create a new app.
3. Connect your GitHub repo.
4. Set your environment variables in the Koyeb dashboard.
5. Deploy!

---

### Deploy on Heroku

1. Fork this repo.
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
3. Create a new Heroku app:
    ```bash
    heroku create your-app-name
    ```
4. Set your config vars:
    ```bash
    heroku config:set API_ID=your_api_id API_HASH=your_api_hash BOT_TOKEN=your_bot_token MONGO_URI=your_mongodb_uri ADMINS=your_admin_id
    ```
5. Push your code:
    ```bash
    git push heroku main
    ```
6. Your bot will start automatically.

---

## My Favorite Waifu Pics

![Miku Nakano](https://wallpaper.forfun.com/fetch/72/72d9ab0c3dfa4777c626ce6b8e056742.jpeg)
![Miku Nakano](https://images7.alphacoders.com/132/1323209.jpeg)
![Miku Nakano](https://images6.alphacoders.com/132/1323207.jpeg)

---

## Community

- Updates Channel: [@ALLHQC](https://t.me/ALLHQC)
- Support Group: [@ALLHQC_Support](https://t.me/ALLHQC_Support)

---

## Credits

- Powered by [Pyrogram](https://docs.pyrogram.org/) and [MongoDB](https://www.mongodb.com/).
- Miku Nakano images © respective artists.
- **Speical Thanks to [DARKXSIDE78](https://t.me/DARKXSIDE78) for creating this bot!**

---

**Enjoy your safe and smart channel
