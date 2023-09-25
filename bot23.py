import telebot
from config2 import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}! Я помогу тебе конвертировать валюты. Напиши мне запрос в формате: <из какой валюты> <в какую валюту> <число для конвертации>.\n Например: евро рубль 100\n Чтобы увидеть список доступных валют нажми /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}! Для начала работы жми /start\n Чтобы увидеть список доступных валют нажми /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'{amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)