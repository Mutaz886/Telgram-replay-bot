
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json
import os

DATA_FILE = "replies.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        replies = json.load(f)
else:
    replies = {}

def save_replies():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(replies, f, ensure_ascii=False)

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم الأمر: /add الكلمة=الرد")
        return
    try:
        data = " ".join(context.args)
        trigger, response = data.split("=")
        replies[trigger.strip()] = response.strip()
        save_replies()
        await update.message.reply_text(f"تم إضافة الرد:
إذا كتب حدا: {trigger}
برد عليه: {response}")
    except:
        await update.message.reply_text("تأكد من الصيغة: /add الكلمة=الرد")

async def delete_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم الأمر: /delete الكلمة")
        return
    trigger = " ".join(context.args).strip()
    if trigger in replies:
        del replies[trigger]
        save_replies()
        await update.message.reply_text(f"تم حذف الرد المرتبط بـ: {trigger}")
    else:
        await update.message.reply_text("ما لقيت رد مرتبط بهاي الكلمة.")

async def list_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not replies:
        await update.message.reply_text("ما في ردود محفوظة حالياً.")
    else:
        text = "\n".join([f"{k} => {v}" for k, v in replies.items()])
        await update.message.reply_text(f"الردود الحالية:\n{text}")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    if message in replies:
        await update.message.reply_text(replies[message])

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

app.add_handler(CommandHandler("add", add_reply))
app.add_handler(CommandHandler("delete", delete_reply))
app.add_handler(CommandHandler("list", list_replies))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_reply))

app.run_polling()
