import telebot
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name

    text = f"""
╔═━━━✦ 🤖 BOT WELCOME ✦━━━═╗

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
    url = message.text.strip()

    try:
        bot.reply_to(message, "⏳ Downloading...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        if not os.path.exists(file_name):
            bot.reply_to(message, "❌ File not found!")
            return

        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_name)

    except Exception as e:
        print(e)
        bot.reply_to(message, "❌ Download failed!")

# ================= RUN =================
print("🤖 Bot running...")
bot.infinity_polling()
