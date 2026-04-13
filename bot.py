import telebot
import yt_dlp
import os

# TOKEN from Railway
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name

    text = f"""
╔═━━━✦ 🤖 𝗕𝗢𝗧 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 ✦━━━═╗

👋 Assalamu Alaikum {name}!

🎬 Video Downloader Bot

━━━━━━━━━━━━━━━━━━
📥 Supported:
➤ TikTok 🎵  
➤ Facebook 📘  
➤ YouTube ▶️  
➤ Instagram 📸  
━━━━━━━━━━━━━━━━━━

🔗 Just send your video link  
⚡ I’ll download it instantly!

💎 Fast | Smooth | Free

👨‍💻 Owner: @JAHIDVAI12

╚═━━━✦ 🚀 ENJOY ✦━━━═╝
"""

    bot.reply_to(message, text, parse_mode="Markdown")

# ================= LINK CHECK =================
def is_link(message):
    return message.text and message.text.startswith("http")

# ================= DOWNLOAD =================
@bot.message_handler(func=is_link)
def download_video(message):
    url = message.text

    try:
        bot.reply_to(message, "⏳ Downloading...")

        ydl_opts = {
            'format': 'best[filesize<50M]',
            'outtmpl': '%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        if not os.path.exists(file_name):
            return

        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_name)

    except Exception as e:
        print(e)

# ================= RUN =================
print("🤖 Bot running...")
bot.infinity_polling()
