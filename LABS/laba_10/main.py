import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TELEGRAM_TOKEN = '7989595985:AAHhbo2Uww5ZGna8H0dDmOYR4n8QFu-7yoQ'
VK_ACCESS_TOKEN = 'vk1.a.gwkaMXOEfF-bUxhSdx26kRcWVJoQIjNa5rg3YGPA_0-sMXMkgbMEyeJNiLMVAjo-nIoGd_zlzARP9uGil6EnFeXgm9iMFV8ak27jup_hfov29mmBozG611CgjIST-y7D9d1fVeUxM7CsvRP6DbKyHRxAIxxfqBlcqZbmNt-nolGSq1Myy470wW27FWsa_BSV'
VK_USER_ID = '340553765'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправь мне сообщение, и я поставлю его в твой статус в VK.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    set_status(text)
    
    await update.message.reply_text('Статус успешно поставлен!')

def set_status(text: str) -> None:
    url = 'https://api.vk.com/method/status.set'
    params = {
        'text': text,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    if response.json().get('error'):
        print(f"Ошибка при установке статуса: {response.json()['error']}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()