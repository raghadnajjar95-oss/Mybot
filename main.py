import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipedia
from keep_alive import keep_alive   # ⬅️ أضفنا هذا السطر

# تفعيل اللغة العربية في البداية
wikipedia.set_lang("ar")

# إعداد اللوجز
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة /start
def start(update, context):
    update.message.reply_text("👋 أهلاً! أرسل لي كلمة وأنا ببحث لك عنها في ويكيبيديا 🔎")

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
            update.message.reply_text("❌ ما لقيت صفحة بهالاسم لا بالعربي ولا بالإنكليزي.")
        except Exception as e:
            update.message.reply_text("⚠️ صار خطأ، جرّب كلمة ثانية.")
    except Exception as e:
        update.message.reply_text("⚠️ صار خطأ غير متوقع، جرّب كلمة ثانية.")

def main():
    # ⚠️ لا تنسي تبدلي YOUR_TOKEN بالتوكن تبع البوت
    updater = Updater("8465989377:AAFo_F7lNwQIIwQTC4DEynDQaOqWhAhoiPI", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))

    keep_alive()  # ⬅️ استدعاء الوظيفة الجديدة (يبقي Replit صاحي)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()