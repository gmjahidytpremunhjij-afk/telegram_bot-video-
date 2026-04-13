import telebot
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "👋 আসসালামু আলাইকুম!\n\n"
        "🎬 ভিডিও ডাউনলোড করতে লিংক পাঠান:\n"
        "✔ TikTok\n✔ Facebook\n✔ YouTube\n✔ Instagram"
    )

# LINK CHECK
def is_link(message):
    return message.text and message.text.startswith("http")

# DOWNLOAD
@bot.message_handler(func=is_link)
def download_video(message):
    url = message.text

    try:
        bot.reply_to(message, "⏬ ডাউনলোড হচ্ছে...")

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

# RUN
print("🤖 Bot running...")
bot.infinity_polling()
