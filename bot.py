import telebot
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name

    text = f"""
╔═══❖ 🤖 WELCOME ❖═══╗

👋 আসসালামু আলাইকুম {name} স্যার!

🎬 *Video Downloader Bot*

━━━━━━━━━━━━━━━
📥 Supported:
✔ TikTok
✔ Facebook
✔ YouTube
✔ Instagram
━━━━━━━━━━━━━━━

🔗 শুধু ভিডিও লিংক পাঠান  
⏬ আমি ডাউনলোড করে দিবো!

👨‍💻 Created by: @JAHIDVAI12

╚════════════════════╝
"""

    bot.reply_to(message, text, parse_mode="Markdown")

# LINK CHECK
def is_link(message):
    return message.text and message.text.startswith("http")

# DOWNLOAD
@bot.message_handler(func=is_link)
def download_video(message):
    url = message.text

    try:
        bot.reply_to(message, "⏳ ডাউনলোড হচ্ছে...")

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
            bot.reply_to(message, "❌ ফাইল পাওয়া যায়নি!")
            return

        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_name)

    except Exception as e:
        print(e)
        bot.reply_to(message, "❌ ডাউনলোড করতে সমস্যা হয়েছে!")

# WRONG MESSAGE
@bot.message_handler(func=lambda m: True)
def wrong(message):
    bot.reply_to(message, "❌ শুধু ভিডিও লিংক পাঠান!")

# RUN BOT
print("🤖 Bot running...")
bot.infinity_polling()
