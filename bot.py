from telebot import TeleBot

from telebot import types

from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")


from markups import (
    main_markup,
    services_markup,
    categories_markup,
)

from services import salon_services

from database import (
    create_engine,
    create_tables,
    DBManager,
)

engine = create_engine(
    user=getenv("DB_USER"),
    password=getenv("PASSWORD"),
    host=getenv("HOST"),
    database=getenv("DATABASE")
)


bot = TeleBot(getenv("TOKEN"))
manager = DBManager(enigne=engine)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    text = """
    Привет, пользователь! Рад тебя видеть.
    Я - телеграм бот салона красоты "Женские секреты"
    Я могу показать тебе наши последние работы, показать прайс услуг
    И зарегистрировать вас на какую-либо процедуру!

    Для более подробной информации отправьте команду /help
    """

    markup = main_markup()

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message: types.Message):
    text = """
    Comming soon!
    """

    bot.send_message(chat_id=message.chat.id, text=text)



@bot.callback_query_handler(lambda call: call.data=="categories")
def get_categories(call: types.CallbackQuery):
    text = """
    Выберите одну из категорий:
    """

    categories = manager.get_all_categories()
    markup = categories_markup(categories=categories)

    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(lambda call: call.data.startswith("category:/"))
def get_services(call: types.CallbackQuery):
    id_ = int(call.data.replace("category:/", ""))
    services = manager.get_services_by_category(category_id=id_)
    markup = services_markup(services=services)

    text = f"Наши услуги по категории:"

    bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



@bot.callback_query_handler(lambda call: call.data.startswith("service:/"))
def get_service(call: types.CallbackQuery):
    id_ = int(call.data.replace("service:/", ""))
    service = manager.get_service(service_id=id_)

    text = f"""
    {service.name} - от {service.price}
    {service.description}
    """

    bot.send_message(chat_id=call.message.chat.id, text=text)

   
@bot.callback_query_handler(lambda call: call.data.startswith("back_to:/"))
def back_to(call: types.CallbackQuery):
    to = call.data
    if to.endswith("categories"):
        return get_categories(call)

if __name__ == "__main__":
    create_tables(engine=engine)
    bot.infinity_polling()