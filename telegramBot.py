import telebot
from nurbaBot.db import create_table

bot = telebot.TeleBot('1241193961:AAGTZCN0oqsVwFtn9rsyitQM48TfgNK00mM')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Привет', 'Пока')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
    create_table(message.chat.id)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'frog':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJchV-2gdzFQ_o8NgbJts8wgDGF7R6zAAJoAAPBnGAMjCWf833RMLEeBA')


@bot.message_handler(commands=['admin'])
def admin_message(message):
    bot.send_message(message.chat.id, 'Введите пароль', reply_markup=keyboard1)
    create_table(message.chat.id)



bot.polling()

# @bot.message_handler(content_types=['text'])
# def lalala(message):                                  эхо бот
#     bot.send_message(message.chat.id, message.text)
