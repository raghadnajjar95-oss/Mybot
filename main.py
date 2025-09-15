import imghdr_pure as imghdr
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import wikipedia

# إعداد اللوج للتجربة
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# دالة /start
def start(update, context):
    update.message.reply_text('👋 أهلاً بك! اكتب أي كلمة وسأجلب لك معلومات من ويكيبيديا.')

# دالة /help
def help_command(update, context):
    update.message.reply_text('ℹ️ أرسل كلمة أو جملة وسأبحث عنها في ويكيبيديا.')

# دالة البحث في ويكيبيديا
def search_wiki(update, context):
    query = update.message.text
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=False, redirect=True)
        update.message.reply_text(summary)
    except Exception as e:
        update.message.reply_text("⚠️ لم أتمكن من إيجاد معلومات، جرّب كلمة أخرى.")

def main():
    # تأكدي أنك ضايفة BOT_TOKEN في Render → Environment
    token = os.getenv("BOT_TOKEN")  
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_wiki))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
