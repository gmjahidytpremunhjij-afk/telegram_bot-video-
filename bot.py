import telebot
import yt_dlp
import os

# TOKEN from Railway
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================= START MESSAGE =================
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name

    text = f"""
╔═━━━✦ 🤖 𝗕𝗢𝗧 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 ✦━━━═╗

👋 𝗔𝘀𝘀𝗮𝗹𝗮𝗺𝘂 𝗔𝗹𝗮𝗶𝗸𝘂𝗺 {name}!

🎬 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁

━━━━━━━━━━━━━━━━━━
📥 𝗦𝘂𝗽𝗽𝗼𝗿𝘁𝗲𝗱 𝗦𝗶𝘁𝗲𝘀:
➤ TikTok 🎵  
➤ Facebook 📘  
➤ YouTube ▶️  
➤ Instagram 📸  
━━━━━━━━━━━━━━━━━━

🔗 𝗝𝘂𝘀𝘁 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝘃𝗶𝗱𝗲𝗼 𝗹𝗶𝗻𝗸  
⚡ 𝗜’𝗹𝗹 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗶𝘁 𝗶𝗻𝘀𝘁𝗮𝗻𝘁𝗹𝘆!

💎 𝗙𝗮𝘀𝘁 | 𝗦𝗺𝗼𝗼𝘁𝗵 | 𝗙𝗿𝗲𝗲

👨‍💻 𝗢𝘄𝗻𝗲𝗿: @JAHIDVAI12

╚═━━━✦ 🚀 𝗘𝗡𝗝𝗢𝗬 ✦━━━═╝
"""

    bot.reply_to(message, text, parse_mode="Markdown")

# ================= HELP =================
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(
        message,
        "📌 শুধু ভিডিও লিংক পাঠান\n🎬 আমি ডাউনলোড করে দিবো 😎",
        parse_mode="Markdown"
    )

# ================= LINK CHECK =================
def is_link(message):
    return message.text and message.text.startswith("http")

# ================= DOWNLOAD =================
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

# ================= WRONG INPUT =================
@bot.message_handler(func=lambda m: True)
def wrong(message):
    bot.reply_to(
        message,
        "❌ শুধু ভিডিও লিংক পাঠান!\n🔗 অন্য কিছু দিলে কাজ করবে না 😅"
    )

# ================= RUN =================
print("🤖 Bot running...")
bot.infinity_polling()
