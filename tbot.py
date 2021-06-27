try:
    import time
    import telebot
    import sqlite3
except:
    import pip
    pip.main(["install", "pyTelegramBotAPI", "time", "sqlite3"])
    import time
    import telebot
    import sqlite3

bot_name = "tbot"
bot = telebot.TeleBot("1852900811:AAGfIUHEcNJx101lPcOAq1aLIyM2MsQHxGk")
link_channel = "https://t.me/joinchat/_bYsD4qEnyJmNDMy"

# Логирование бота
def write_log(event):
    is_bot = "person"
    if event.from_user.is_bot: is_bot = "bot"
    log = time.strftime(f"%d.%m.%Y %H:%M:%S @{event.from_user.username} {is_bot} {event.from_user.language_code}\n")
    with open(f"./log/{bot_name}.log", "a") as w:
        w.write(log)
        w.close()

# Настраиваем БД.
def get_connection(name_db:str = "file.db"):
    connect = sqlite3.connect(name_db)
    return(connect)

def init_db(force:bool = False):
    connect = get_connection()
    c = connect.cursor()
    if force:
        c.execute("""
            DROP TABLE IF NOT EXIST user_message
        """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_message (
            id        INTEGER PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            text      TEXT NOT NULL
        )
    """)
    connect.commit()

def add_message(user_id: int, text: str):
    connect = get_connection()
    c = connect.cursor()
    c.execute("INSERT INTO user_message (user_id, text) VALUES (?, ?)", (user_id, text))
    connect.commit()

init_db()
add_message(user_id=1, text="HELLO MYSQL!")

@bot.message_handler(commands=["start"])
def start(message):
    #bot.send_animation(message.chat.id, gif, caption="GIF")
    write_log(message)
    start_img = open("content/imgs/1.png", "rb")
    bot.send_photo(message.chat.id, start_img, caption=f"Здравствуйте {message.from_user.first_name}, тут должен быть текст приветствия или описания меню, а также, соответственно, другая картинка.")

    # Обозначение клавиатуры
    keyboard = telebot.types.InlineKeyboardMarkup()

    # Кнопки
    key1 = telebot.types.InlineKeyboardButton(text="Электронное меню", callback_data="menu")
    key2 = telebot.types.InlineKeyboardButton(text="Список цен", callback_data="price_list")
    key3 = telebot.types.InlineKeyboardButton(text="Помощь", callback_data="help")
    key4 = telebot.types.InlineKeyboardButton(text="Связаться с нами", callback_data="contact")
    key5 = telebot.types.InlineKeyboardButton(text="Оставить отзыв", callback_data="comment")
    key6 = telebot.types.InlineKeyboardButton(text="Мои покупки", callback_data="my_purchases")

    # Добавление кнопок на клавиатуру
    keyboard.add(key1, key2)
    keyboard.add(key3, key4)
    keyboard.add(key5, key6)
    bot.send_message(message.chat.id, text=f"Узнайте больше о том, что умеет {bot_name}", reply_markup=keyboard)

@bot.message_handler(commands=["menu"])
def menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    key1 = telebot.types.InlineKeyboardButton(text="Выпечка", callback_data="выпечка")
    key2 = telebot.types.InlineKeyboardButton(text="Десерты", callback_data="десерты")
    key3 = telebot.types.InlineKeyboardButton(text="Напитки", callback_data="напитки")
    keyboard.add(key1, key2, key3)
    #msg = bot.send_message(message.chat.id, text="Тестовое меню:\n1. Борщ\n2. Гречка\n3. Компот\nВыберите номер из списка")#, reply_markup=keyboard)
    #if msg.text in ["1", "2", "3"]:
    #    bot.register_next_step_handler(msg, test)
    #else:
    #    bot.send_message(message.chat.id, text="Нет такого блюда! Попробуйте ещё раз.")
    bot.send_message(message.chat.id, text="Выберите то что хотите заказать!", reply_markup=keyboard)

@bot.message_handler(commands=["price_list"])
def price_list(message):
    bot.send_message(message.chat.id, text="Тестовое меню:\n1. Борщ: 5р\n2. Гречка: 5р\n3. Компот: 3р")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, text="Доступные на данный момент команды:\n/start\n/help\n/menu\n/contact\n/price_list\n/comment\n/my_purchases")

@bot.message_handler(commands=["contact"])
def contact(message):
    bot.send_message(message.chat.id, text=f"Обращайтесь по адресу {link_channel}")

@bot.message_handler(commands=["comment"])
def comment(message):
    msg = bot.send_message(message.chat.id, text="Напишите свой отзыв")
    #bot.register_next_step_handler(msg, "text")

@bot.message_handler(commands=["my_purchases"])
def my_purchases(message):
    bot.send_message(message.chat.id, text="Мои покупки:\n1. 28.04.2021 17:29:43  Гречка(x3) - 15р\n   [Оплата по карте радуга]")

@bot.callback_query_handler(func=lambda call: True)
def callbacker(call):
    if call.data == "help":
        help(call.message)
    elif call.data == "menu":
        menu(call.message)
    elif call.data == "contact":
        contact(call.message)
    elif call.data == "price_list":
        price_list(call.message)
    elif call.data == "comment":
        comment(call.message)
    elif call.data == "my_purchases":
        my_purchases(call.message)
    elif call.data == "make_order":
        test(call.message)
    elif call.data == "выпечка":
        bot.register_next_step_handler(call.message, "Меню на сегодня")
        bot.register_next_step_handler(call.message, "Отличный выбор! 👍")


#@bot.message_handler(content_types=["text"])
#def text(message):
#    if (message.text == "test"):
#        msg = bot.send_message(message.chat.id, text="Enter any message")
#        bot.register_next_step_handler(msg, test)
#
#def test(message):
#    try:
#        bot.reply_to(message, "Its working")
#    except Exception as e:
#        bot.reply_to(message, "oooops")

def test(msg):
    print(msg.text)
    msg = bot.send_message(msg.chat.id, text="Спасибо! Отличный выбор!")
    bot.register_next_step_handler(msg, test1)

def test1(msg):
    print("Yes!")

bot.polling()
