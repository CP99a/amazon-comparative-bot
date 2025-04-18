import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from image_builder import generate_comparative_image
from amazon_scraper import get_two_images_from_amazon
import tempfile
import os

TOKEN = "7542976774:AAHrOuImOzDDKroDuqBYFhlVaAE4M08zPRY"

logging.basicConfig(level=logging.INFO)

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📦 Inviami fino a 4 link Amazon. Io scaricherò 2 immagini da ciascuno e ti restituirò una comparativa 1:1!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if chat_id not in user_sessions:
        user_sessions[chat_id] = []

    links = text.split()
    valid_links = [l for l in links if "amazon." in l]

    if not valid_links:
        await update.message.reply_text("⚠️ Nessun link Amazon trovato.")
        return

    user_sessions[chat_id].extend(valid_links)

    if len(user_sessions[chat_id]) >= 4:
        await update.message.reply_text("🔄 Generazione in corso, attendi qualche secondo...")

        all_images = []
        for link in user_sessions[chat_id][:4]:
            imgs = await get_two_images_from_amazon(link)
            all_images.extend(imgs)

        output_path = tempfile.mktemp(suffix=".jpg")
        generate_comparative_image(all_images, output_path)

        with open(output_path, 'rb') as img:
            await update.message.reply_photo(photo=img, caption="✅ Ecco la tua comparativa!")

        user_sessions[chat_id] = []
        os.remove(output_path)
    else:
        await update.message.reply_text(f"✅ Link ricevuti: {len(user_sessions[chat_id])}/4. Inviami gli altri!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
