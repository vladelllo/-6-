Задание
Создать меню (клавиатуру) для вашего бота. Модифицируйте текст пунктов меню, не используйте примеры из теории ниже. На нажатие каждой клавиши должен выдаваться ответ, глубина вложенности вопросов и ответов должна быть не меньше двух, т.е. на первый ответ пользователя бот присылает новую клавиатуру с новыми вопросами. Всего различных клавиш должно быть не меньше восьми.
Создать инлайн-клавиатуру для вашего бота. Результаты выбора должны фиксироваться.

Дополнительное задание
Вывести счётчик нажатий каждой клавиши
Под сообщением от бота должно быть два выбора: «Мне нравится» и «Мне не нравится» с счётчиком нажатий, а также создана кнопка статистики выборов

Реализация
Напишем код бота с меню, который будет помогать выбрать город для отпуска в зависимости от пожеланий пользователя, на языке питон. Также реализуем счетчик нажатий клавиш для тех, где нажатий больше 3.
Напишем код бота с инлайн-меню на питоне, который будет предлагать два выбора на каждое свое сообщение: «Мне нравится» и «Мне не нравится», а также будет иметь счетчик нажатий данных кнопок. За основу возьмем бота из предыдущей лабораторной работы.

Код 
import telebot
from telebot import types

TOKEN = '7989595985:AAHhbo2Uww5ZGna8H0dDmOYR4n8QFu-7yoQ'
bot = telebot.TeleBot(TOKEN)

button_stats = {
    'Главное меню': {
        '🏔️ Города': 0,
        '🏛️ Достопримечательности': 0,
        '🍲 Кухня': 0,
        '🚆 Транспорт': 0
    },
    'Города': {
        'Москва': 0,
        'Санкт-Петербург': 0,
        'Казань': 0,
        'Сочи': 0,
    },
    'Достопримечательности': {
        'Красная площадь': 0,
        'Эрмитаж': 0,
        'Озеро Байкал': 0,
        'Долина гейзеров': 0,
    },
    'Еда': {
        'Блюда': 0,
        'Напитки': 0,
        'Десерты': 0,
    },
    'Транспорт': {
        'Авиа': 0,
        'ЖД': 0,
        'Автобусы': 0,
    }
}

inline_button_stats = {
    'like': 0,
    'dislike': 0,
    'user_choices': {},  # {user_id: 'like'/'dislike'}
    'asked_users': set()  # Множество пользователей, которым уже задавали вопрос
}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🏔️ Города')
    btn2 = types.KeyboardButton('🏛️ Достопримечательности')
    btn3 = types.KeyboardButton('🍲 Кухня')
    btn4 = types.KeyboardButton('🚆 Транспорт')
    btn5 = types.KeyboardButton('/stats')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def cities_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Москва')
    btn2 = types.KeyboardButton('Санкт-Петербург')
    btn3 = types.KeyboardButton('Казань')
    btn4 = types.KeyboardButton('Сочи')
    btn5 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def attractions_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Красная площадь')
    btn2 = types.KeyboardButton('Эрмитаж')
    btn3 = types.KeyboardButton('Озеро Байкал')
    btn4 = types.KeyboardButton('Долина гейзеров')
    btn5 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def cuisine_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Блюда')
    btn2 = types.KeyboardButton('Напитки')
    btn3 = types.KeyboardButton('Десерты')
    btn4 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def transport_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Авиа')
    btn2 = types.KeyboardButton('ЖД')
    btn3 = types.KeyboardButton('Автобусы')
    btn4 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def send_inline_message(chat_id, user_id):
    # Проверяем, задавали ли уже вопрос этому пользователю
    if user_id in inline_button_stats['asked_users']:
        return

    inline_button_stats['asked_users'].add(user_id)
    user_choice = inline_button_stats['user_choices'].get(user_id)

    keyboard = types.InlineKeyboardMarkup()

    like_text = "👍 Мне нравится"
    dislike_text = "👎 Мне не нравится"

    if user_choice == 'like':
        like_text += " (Ваш выбор)"
    elif user_choice == 'dislike':
        dislike_text += " (Ваш выбор)"

    like_button = types.InlineKeyboardButton(
        text=f"{like_text} ({inline_button_stats['like']})",
        callback_data='like'
    )
    dislike_button = types.InlineKeyboardButton(
        text=f"{dislike_text} ({inline_button_stats['dislike']})",
        callback_data='dislike'
    )

    keyboard.add(like_button, dislike_button)
    message_text = "Понравился ли вам бот?"
    bot.send_message(chat_id, message_text, reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🇷🇺 Добро пожаловать в бота 'Путешествия по России'!", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_keyboard(call):
    user_id = call.from_user.id
    current_choice = inline_button_stats['user_choices'].get(user_id)

    if call.data == 'like':
        if current_choice != 'like':
            inline_button_stats['like'] += 1
            if current_choice == 'dislike':
                inline_button_stats['dislike'] -= 1
            inline_button_stats['user_choices'][user_id] = 'like'
    elif call.data == 'dislike':
        if current_choice != 'dislike':
            inline_button_stats['dislike'] += 1
            if current_choice == 'like':
                inline_button_stats['like'] -= 1
            inline_button_stats['user_choices'][user_id] = 'dislike'

    keyboard = types.InlineKeyboardMarkup()

    like_text = "👍 Мне нравится"
    dislike_text = "👎 Мне не нравится"

    user_choice = inline_button_stats['user_choices'].get(user_id)
    if user_choice == 'like':
        like_text += " (Ваш выбор)"
    elif user_choice == 'dislike':
        dislike_text += " (Ваш выбор)"

    like_button = types.InlineKeyboardButton(
        text=f"{like_text} ({inline_button_stats['like']})",
        callback_data='like'
    )
    dislike_button = types.InlineKeyboardButton(
        text=f"{dislike_text} ({inline_button_stats['dislike']})",
        callback_data='dislike'
    )

    keyboard.add(like_button, dislike_button)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Понравился ли вам бот?",
        reply_markup=keyboard
    )

@bot.message_handler(content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text

    for category, buttons in button_stats.items():
        if text in buttons:
            button_stats[category][text] += 1

    if text == '🏔️ Города':
        bot.send_message(chat_id, "Выберите город:", reply_markup=cities_menu())
    elif text == '🏛️ Достопримечательности':
        bot.send_message(chat_id, "Знаменитые достопримечательности России:", reply_markup=attractions_menu())
    elif text == '🍲 Кухня':
        bot.send_message(chat_id, "Русская кухня:", reply_markup=cuisine_menu())
    elif text == '🚆 Транспорт':
        bot.send_message(chat_id, "Транспорт в России:", reply_markup=transport_menu())

    elif text == 'Москва':
        response = """🏙️ Москва - столица России!
Основные места:
• Красная площадь
• Кремль
• ВДНХ
• Парк Горького
Рекомендуем посетить Третьяковскую галерею!"""
        bot.send_message(chat_id, response)
    elif text == 'Санкт-Петербург':
        response = """🌉 Санкт-Петербург - культурная столица!
Обязательно посетите:
• Эрмитаж
• Петергоф
• Исаакиевский собор
• Невский проспект
Не пропустите развод мостов!"""
        bot.send_message(chat_id, response)
    elif text == 'Казань':
        response = """🕌 Казань - город контрастов!
Интересные места:
• Казанский Кремль
• Мечеть Кул-Шариф
• Храм всех религий
• Баскетбольный клуб "Зенит"
Попробуйте эчпочмак - местное блюдо!"""
        bot.send_message(chat_id, response)
    elif text == 'Сочи':
        response = """🌴 Сочи - курортная столица!
Чем заняться:
• Парк "Ривьера"
• Красная Поляна
• Олимпийский парк
• Сочинский дендрарий
Отличное место для отдыха круглый год!"""
        bot.send_message(chat_id, response)

    elif text == 'Красная площадь':
        bot.send_message(chat_id,
                         "❤️ Красная площадь - сердце России. Здесь находятся: Кремль, Мавзолей, ГУМ и Собор Василия Блаженного.")
    elif text == 'Эрмитаж':
        bot.send_message(chat_id,
                         "🏛️ Эрмитаж - один из крупнейших музеев мира. Коллекция включает более 3 млн экспонатов!")
    elif text == 'Озеро Байкал':
        bot.send_message(chat_id,
                         "💧 Байкал - самое глубокое озеро на планете (1642 м). Содержит 20% мировых запасов пресной воды!")
    elif text == 'Долина гейзеров':
        bot.send_message(chat_id,
                         "🌋 Долина гейзеров на Камчатке - единственное гейзерное поле в Евразии. Открыто в 1941 году.")

    elif text == 'Блюда':
        response = """🍽️ Топ-5 русских блюд:
1. Борщ - свекольный суп
2. Пельмени - мясные вареники
3. Блины с разными начинками
4. Оливье - традиционный салат
5. Бефстроганов - мясо в сметанном соусе"""
        bot.send_message(chat_id, response)
    elif text == 'Напитки':
        response = """🍹 Популярные напитки:
• Квас - хлебный напиток
• Морс - ягодный напиток
• Сбитень - традиционный горячий напиток
• Чай из самовара"""
        bot.send_message(chat_id, response)
    elif text == 'Десерты':
        response = """🍰 Русские сладости:
• Пряники
• Пастила
• Халва
• Сгущенка
• Шарлотка"""
        bot.send_message(chat_id, response)

    elif text == 'Авиа':
        bot.send_message(chat_id,
                         "✈️ Основные авиакомпании: Аэрофлот, S7, Уральские авиалинии. Билеты лучше покупать заранее.")
    elif text == 'ЖД':
        bot.send_message(chat_id,
                         "🚂 Российские железные дороги (РЖД) - удобный способ путешествовать. Есть скоростные поезда (Сапсан, Ласточка).")
    elif text == 'Автобусы':
        bot.send_message(chat_id,
                         "🚌 Междугородние автобусы доступны между всеми крупными городами. Компании: Busfor, Ecolines.")

    elif text == 'Назад':
        bot.send_message(chat_id, "Возвращаемся в главное меню", reply_markup=main_menu())
        send_inline_message(chat_id, user_id)

    elif text == '/stats':
        stats = "📊 Статистика нажатий (только пункты с 3+ нажатиями):\n"

        # Обрабатываем обычные кнопки
        for category, buttons in button_stats.items():
            category_stats = []
            for btn, count in buttons.items():
                if count >= 3:
                    category_stats.append(f"{btn}: {count}")

            if category_stats:
                stats += f"\n{category}:\n" + "\n".join(category_stats)

        if stats.strip() == "📊 Статистика нажатий (только пункты с 3+ нажатиями):":
            stats = "Пока нет статистики по нажатиям (нужно минимум 3 нажатия на пункт)"

        bot.send_message(chat_id, stats)

    else:
        bot.send_message(chat_id, "Используйте кнопки меню для навигации", reply_markup=main_menu())

if __name__ == '__main__':
    print("Бот 'Путешествия по России' запущен...")
    bot.polling(none_stop=True)
