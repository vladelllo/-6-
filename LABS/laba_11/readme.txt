Задание
Телеграм бот должен выдавать курс валюты по отношению к рублю. Валюта выбирается преподавателем. Дата вводится пользователем с клавиатуры 

Дополнительно
Бот должен иметь клавиатуру с выбором из не менее чем 2 разных валют

Реализация
Напишем код бота с меню на питоне, который будет иметь возможность выводить курс выбранной пользователем в меню валюты в определенную дату.
Выберем 3 валюты: доллар, евро, китайский юань и реализуем клавиатуру с выбором валюты, а также пропишем обработчик ошибок в случае ввода неправильной даты.

Код
import xml.dom.minidom
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7989595985:AAHhbo2Uww5ZGna8H0dDmOYR4n8QFu-7yoQ"
CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp?date_req="
CURRENCIES = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'CNY': 'Китайский юань'
}

SELECT_CURRENCY, SELECT_START_DATE, SELECT_END_DATE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[currency] for currency in CURRENCIES.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот для получения курсов валют ЦБ РФ.\n"
        "Выбери валюту:",
        reply_markup=reply_markup
    )
    return SELECT_CURRENCY

async def select_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text not in CURRENCIES:
        await update.message.reply_text("Пожалуйста, выберите валюту из предложенных вариантов")
        return SELECT_CURRENCY
    
    context.user_data['currency'] = text
    await update.message.reply_text(
        f"Выбрана валюта: {CURRENCIES[text]}\n"
        "Введите начальную дату периода в формате ДД.ММ.ГГГГ:"
    )
    return SELECT_START_DATE

async def select_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        date = datetime.strptime(text, "%d.%m.%Y").date()
        if date > datetime.now().date():
            await update.message.reply_text("Дата не может быть в будущем. Введите корректную дату:")
            return SELECT_START_DATE
            
        context.user_data['start_date'] = text
        await update.message.reply_text("Введите конечную дату периода в формате ДД.ММ.ГГГГ:")
        return SELECT_END_DATE
    except ValueError:
        await update.message.reply_text("Неверный формат даты. Введите дату в формате ДД.ММ.ГГГГ:")
        return SELECT_START_DATE

async def select_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        start_date = datetime.strptime(context.user_data['start_date'], "%d.%m.%Y").date()
        end_date = datetime.strptime(text, "%d.%m.%Y").date()
        
        if end_date < start_date:
            await update.message.reply_text("Конечная дата не может быть раньше начальной. Введите корректную дату:")
            return SELECT_END_DATE
        if end_date > datetime.now().date():
            await update.message.reply_text("Дата не может быть в будущем. Введите корректную дату:")
            return SELECT_END_DATE
            
        if (end_date - start_date).days > 365:
            await update.message.reply_text("Период не должен превышать 1 год. Введите меньший период:")
            return SELECT_END_DATE
            
        context.user_data['end_date'] = text
        
        # Получаем данные
        currency = context.user_data['currency']
        start_date_str = context.user_data['start_date']
        end_date_str = context.user_data['end_date']
        dates, rates = get_currency_rates_for_period(currency, start_date_str, end_date_str)
        
        if not dates:
            await update.message.reply_text("Не удалось получить данные за указанный период. Попробуйте другой период.")
            return await start(update, context)
            
        # Создаем красивый график
        plt.figure(figsize=(12, 6))
        
        # Основной график
        line, = plt.plot(dates, rates, marker='o', linestyle='-', 
                        color='#2ecc71', linewidth=2, markersize=6,
                        markerfacecolor='#e74c3c', markeredgecolor='#c0392b')
        
        # Подсветка минимального и максимального значений
        min_rate = min(rates)
        max_rate = max(rates)
        min_date = dates[rates.index(min_rate)]
        max_date = dates[rates.index(max_rate)]
        
        plt.scatter([min_date, max_date], [min_rate, max_rate], 
                   color=['#3498db', '#e74c3c'], s=100, zorder=5)
        
        # Подписи к точкам
        plt.annotate(f'{min_rate:.2f}', xy=(min_date, min_rate), xytext=(5, 5),
                    textcoords='offset points', color='#3498db', fontsize=10)
        plt.annotate(f'{max_rate:.2f}', xy=(max_date, max_rate), xytext=(5, 5),
                    textcoords='offset points', color='#e74c3c', fontsize=10)
        
        # Заполнение под графиком
        plt.fill_between(dates, rates, alpha=0.1, color='#2ecc71')
        
        # Настройки внешнего вида
        plt.title(f"Динамика курса {CURRENCIES[currency]}\n{start_date_str} - {end_date_str}", 
                 fontsize=14, pad=20, color='#34495e')
        plt.xlabel("Дата", fontsize=12, color='#34495e')
        plt.ylabel("Курс, руб.", fontsize=12, color='#34495e')
        
        # Сетка и фон
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.gca().set_facecolor('#f9f9f9')
        
        # Оси
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_color('#bdc3c7')
        plt.gca().spines['bottom'].set_color('#bdc3c7')
        
        # Формат дат на оси X
        plt.gcf().autofmt_xdate()
        
        # Добавляем среднюю линию
        mean_rate = sum(rates)/len(rates)
        plt.axhline(y=mean_rate, color='#9b59b6', linestyle='--', linewidth=1, alpha=0.7)
        plt.annotate(f'Среднее: {mean_rate:.2f}', xy=(dates[-1], mean_rate), 
                    xytext=(5, 5), textcoords='offset points',
                    color='#9b59b6', fontsize=9)
        
        # Сохраняем график
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor=plt.gcf().get_facecolor())
        buf.seek(0)
        plt.close()
        
        # Отправляем график
        await update.message.reply_photo(
            photo=buf,
            caption=f"📈 Курс {CURRENCIES[currency]}:\n"
                   f"➡ Начало: {start_date_str}\n"
                   f"➡ Конец: {end_date_str}\n"
                   f"📊 Минимум: {min_rate:.2f}\n"
                   f"📈 Максимум: {max_rate:.2f}\n"
                   f"🧮 Среднее: {mean_rate:.2f}"
        )
        
        return await start(update, context)
        
    except ValueError:
        await update.message.reply_text("Неверный формат даты. Введите дату в формате ДД.ММ.ГГГГ:")
        return SELECT_END_DATE

def get_currency_rate(currency_code: str, date: str) -> float:
    try:
        response = requests.get(f"{CBR_URL}{date}")
        if response.status_code != 200:
            return None
        
        dom = xml.dom.minidom.parseString(response.text)
        dom.normalize()
        
        valutes = dom.getElementsByTagName("Valute")
        
        for valute in valutes:
            char_code = valute.getElementsByTagName("CharCode")[0]
            if char_code.firstChild.nodeValue == currency_code:
                value = valute.getElementsByTagName("Value")[0].firstChild.nodeValue
                nominal = valute.getElementsByTagName("Nominal")[0].firstChild.nodeValue
                return float(value.replace(',', '.')) / float(nominal)
                
        return None
    except Exception as e:
        print(f"Ошибка при получении курса: {e}")
        return None

def get_currency_rates_for_period(currency_code: str, start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%d.%m.%Y").date()
    end = datetime.strptime(end_date, "%d.%m.%Y").date()
    
    dates = []
    rates = []
    
    current_date = start
    while current_date <= end:
        date_str = current_date.strftime("%d.%m.%Y")
        rate = get_currency_rate(currency_code, date_str)
        
        if rate is not None:
            dates.append(current_date)
            rates.append(rate)
        
        current_date += timedelta(days=1)
    
    return dates, rates

def main():
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_CURRENCY: [
                MessageHandler(filters.Regex(f"^({'|'.join(CURRENCIES.keys())})$"), select_currency)
            ],
            SELECT_START_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_start_date)
            ],
            SELECT_END_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_end_date)
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
