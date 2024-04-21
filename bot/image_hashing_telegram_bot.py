import hashlib
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '6520657010:AAGxxj_822EgHIbjx1bVuEkHrrH7XwHNgE4'
BOT_USERNAME = '@Image_Hash_Bot1'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am the Image Hash Bot.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I will calculate the hash of any image you provide me with.')


def handle_response(text: str) -> str:
    processed: str = text
    if isinstance(processed, str) or isinstance(processed, int):
        return 'Error: I can only receive JPEG or JPG files.'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            response = 'ERRO: can only handle image messages.'
    else:
        response = 'ERRO: can only handle image messages.'

    await update.message.reply_text(response)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message
    doc_file = await document.document.get_file()
    doc_path = doc_file.file_path
    if document.document:
        if document.document.file_name.lower().endswith(('jpg', 'jpeg')):
            #download the photo
            response = requests.get(doc_path)
            doc_data = response.content
            photo_hash = hashlib.sha256(doc_data).hexdigest()
            await document.reply_text(f"Hash of the photo: {photo_hash}")
        else:
            await document.reply_text("ERROR: send me a JPG or JPEG image.")
        
            
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.photo:
        photo_file = await message.photo[-1].get_file()
        photo_path = photo_file.file_path

        # Check if the file extension is JPG or JPEG
        if photo_path.lower().endswith(('.jpg', '.jpeg')):
            # Download the photo
            response = requests.get(photo_path)
            photo_data = response.content
            # Calculate the hash of the photo data
            photo_hash = hashlib.sha256(photo_data).hexdigest()

            await message.reply_text(f"Hash of the photo: {photo_hash}")
        else:
            await message.reply_text("Please send me a JPG or JPEG image.")
    else:
        await message.reply_text("Please send me an image.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_document))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)