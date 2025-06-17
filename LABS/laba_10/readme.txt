Задание
Принять текстовое сообщение от собеседника бота. Отправить его в социальную сеть вконтакте.

Дополнительное задание:
 Поставить это сообщение в статус 

Реализация
Напишем код бота с меню на питоне, который будет иметь возможность ставить в статус текст, введенный пользователем в чате. В целях экономии числа ботов, данный функционал был добавлен к боту из предыдущей лабораторной. 

Код 
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
VK_ACCESS_TOKEN = 'vk1.a.77mmjNjyKTkPFzZkF6dFWFTYBibCKJBSa1LZAlQ9Tr7GiRiZgFsY4EYRvnCri4RhaEXkxkENQbUA44zp1ZOqxBBjuW217LoYdUlsVv0oR7um6WRV5LnGgYTzkZvxPSeP298DvdjhVGYQXOhagYrKDZalo2z_cfAm7dxUtq9TbwVEH2fZ9q39RHY-h-aF3QWfAYEe6kxGVi03_clkXnIJWQ'
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
