import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipedia

# تفعيل اللغة العربية كبداية
wikipedia.set_lang("ar")

# إعداد اللوجز
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة /start
def start(update, context):
    update.message.reply_text("👋 أهلاً! أرسل لي كلمة وسأبحث عنها في ويكيبيديا 🔎")

# دالة البحث
def search(update, context):
    query = update.message.text
    try:
        # البحث بالعربي أولاً
        wikipedia.set_lang("ar")
        result = wikipedia.summary(query, sentences=2)
        update.message.reply_text(result)
    except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
        try:
            # إذا ما لقى بالعربي، يحاول بالإنكليزي
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=2)
            update.message.reply_text(result)
        except wikipedia.exceptions.PageError:
            update.message.reply_text("❌ لم أجد صفحة بهذا الاسم لا بالعربي ولا بالإنكليزي.")
        except Exception:
            update.message.reply_text("⚠️ حدث خطأ، جرّب كلمة أخرى.")
    except Exception:
        update.message.reply_text("⚠️ حدث خطأ غير متوقع، جرّب كلمة أخرى.")

def main():
    # جلب التوكن من Environment Variables
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        print("❌ لم أجد التوكن! تأكد أنك أضفته بالـ Environment Variables باسم BOT_TOKEN")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # الأوامر
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))

    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
