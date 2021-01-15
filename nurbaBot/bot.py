from telebot import types

import telebot
from nurbaBot import setting
from nurbaBot.cinema_parser import  get_cinema_address, get_broadwey
from nurbaBot.db import insert_table, insert_poster, select_category, select_category_where, select_poster, \
    beautifully_poster

bot = telebot.TeleBot(setting.TG_BOT)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('help', 'Категории')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Что умеет делать этот бот?' + '\nЯ покажу тебе все доступные мероприятия в городе Бищкек', reply_markup=keyboard1)
    insert_table(message.chat.id, message.chat.username)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text='Хорошо', callback_data='good')
        item2 = types.InlineKeyboardButton(text='Не очень', callback_data='bad')

        markup.add(item1, item2)

        bot.send_message(message.chat.id, 'Привет, как дела?', reply_markup=markup)

    elif message.text == 'help':
        help = 'Все команды:' + \
               '\nПривет + Пока:  Отвечу на вопрос' + \
               '\nfrog: Стикеры' + \
               '\n/add_poster: Заполнить базу данных' + \
               '\nПосмотреть все' + \
               '\nКатегории' + \
               '\nА еще я сохраняю вашу id и user_id что бы в дальнейшем отправлять вам рекламу'

        bot.send_message(message.chat.id, help)

    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Удачного дня')

    elif message.text.lower() == 'frog':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJchV-2gdzFQ_o8NgbJts8wgDGF7R6zAAJoAAPBnGAMjCWf833RMLEeBA')

    elif message.text == '/add_poster':
        bot.send_message(message.chat.id, 'Напишиет афишу:'
                                          '\nНапример:'
                                          '\nКатегория'
                                          '\nНазвания;'
                                          '\nАддрес;'
                                          '\n2018-11-23 17:31:26;'
                                          '\nссылка к аддресу')

    elif message.text == 'Посмотреть все афиши':
        article_poster = beautifully_poster(select_poster())
        index = len(article_poster) / 7
        i = 1
        while i <= index:
            string_num = str(i)
            string = 'Имя: ' + article_poster['name' + string_num] + \
                     '\nАдрес: ' + article_poster['address' + string_num] + \
                     '\nВремя: ' + article_poster['date_time' + string_num] + \
                     '\nОписание: ' + article_poster['text' + string_num]
            link_location = article_poster['location' + string_num]

            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton(text="2гис", url=link_location)
            markup.add(item1)

            bot.send_message(message.chat.id, string, reply_markup=markup)

            i += 1

    elif message.text == 'Категории':
        list_category = select_category()

        if len(list_category) == 0:
            bot.send_message(message.chat.id, 'Афиш нет')
        else:
            index = 0
            for ctg in select_category():
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton(text=ctg[index], callback_data='//' + ctg[index])
                markup.add(item1)

                index += 1

            bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=markup)

    elif message.text[:1] + message.text[len(message.text):] == '#':  #insert poster
        bot.send_message(message.chat.id, 'Зaгружаю...')
        try:
            s = message.text[1:]  # Удалить символ "#"
            category = s.split(';')[0]  # Разделить полный текст
            name = s.split(';')[1]
            address = s.split(';')[2]
            date_time = s.split(';')[3]
            text = s.split(';')[4]
            location = s.split(';')[5]

            category = category[:0] + category[1:] #delete simbol #

            result = insert_poster(category, name, address, date_time, text, location)
            if result == 1:
                bot.send_message(message.chat.id, 'афиша успешно загружено в базу данных')
            else:
                bot.send_message(message.chat.id, 'что-то пошло не так')
        except UnboundLocalError:
            bot.send_message(message.chat.id, 'Что-то пошло не так')
        except IndexError:
            bot.send_message(message.chat.id, 'Что-то пошло не так')
        else:
            bot.send_message(message.chat.id, 'Что-то пошло не так')

    elif message.text == 'Кинотеатры':
        # markup = types.InlineKeyboardMarkup()
        # for art_cinema in get_broadwey():
        #     markup.add(art_cinema)
        #
        # bot.send_message(message.chat.id, 'Кинотеатры г.Бишкек ', reply_markup=markup)

        for i in get_broadwey():
            bot.send_message(message.chat.id, i)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data[:2] + call.data[len(call.data):] == '//':
                category = call.data[:0] + call.data[2:]
                article_poster = beautifully_poster(select_category_where(category))
                index = len(article_poster) / 7
                i = 1
                while i <= index:
                    string_num = '1'
                    string = 'Имя: ' + article_poster['name' + string_num] + \
                             '\nАдрес: ' + article_poster['address' + string_num] + \
                             '\nВремя: ' + article_poster['date_time' + string_num] + \
                             '\nОписание: ' + article_poster['text' + string_num]
                    link_location = article_poster['location' + string_num]

                    markup = types.InlineKeyboardMarkup()
                    item1 = types.InlineKeyboardButton(text="2гис", url=link_location)
                    markup.add(item1)

                    bot.send_message(call.message.chat.id, string, reply_markup=markup)

                    i += 1

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Категории",
                                      reply_markup=None)

            # elif call.data[:4] + call.data[len(call.data):] == 'http':
            #
            #     address = get_cinema_address(call.data)
            #     bot.send_message(call.message.chat.id, 'Адрес: ' + address['address'] + '\nТелефон: ' + address['cell_number'])
            #
            #     art_movie = parse_movie(call.data)
            #     for art in parse_movie(call.data):
            #         str = '🎬' + art['title'] + \
            #             '\n📶' + art['format'] + \
            #             '\n🕓' + art['time'] + \
            #             '\n💰' + art['price']
            #
            #         markup = types.InlineKeyboardMarkup()
            #         item1 = types.InlineKeyboardButton(text="Перейти на стриницу", url=art['link'])
            #         markup.add(item1)
            #
            #         bot.send_message(call.message.chat.id, str, reply_markup=markup)
            elif call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            else:
                bot.send_message(call.message.chat.id, 'good')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Привет, как дела?",
                                  reply_markup=None)

            # bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False,
            #                           text="Тестовое уведомления")
    except Exception as e:
        print(repr(e))
        print('grgrgr')


bot.polling(none_stop=True)
