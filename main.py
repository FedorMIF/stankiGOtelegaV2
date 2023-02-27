import random

import telebot
import re
import way
from os import listdir
from os.path import isfile, join

bot = telebot.TeleBot('5240511847:AAEHJgb-EJWnzyvp_JE9kq-wFpwf9q0wZ4c')

menu1 = telebot.types.InlineKeyboardMarkup()
menu1.add(telebot.types.InlineKeyboardButton(text = '<', callback_data ='left'))
menu1.add(telebot.types.InlineKeyboardButton(text = '>', callback_data ='right'))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):	
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, ')
                                      #f'я бот, который строит маршрут между аудиториями МГТУ Станкин.')

@bot.message_handler(commands=['sendimg'])
def sen_img(mess):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    bot.send_photo(mess.chat.id, photo=open(f"src/png/{random.choice(onlyfiles)}", 'rb'), caption='Это МТГУ Станкин')

@bot.message_handler(commands=['findway'])
def what_aud(mess):
    ms = bot.send_message(mess.chat.id, 'Напиши номера аудиторий которая рядом и куда надо через пробел')
    bot.register_next_step_handler(ms, make_way)

def make_way(mess):
    auds = (mess.text).split()
    try:
        num1 = auds[0]
        num2 = auds[1]
        if way.pars_build(num1) and way.pars_build(num2):
            bot.send_message(mess.chat.id, f'Маршрут от {auds[0]} до {auds[1]}')
        else:
            mes = bot.send_message(mess.chat.id, 'Какого то номера нет, попробуй другой номер')
            bot.register_next_step_handler(mes, make_way)
    except:
        mes = bot.send_message(mess.chat.id, 'Ты ввел не числа, введи просто два номера аудиторий через пробел')
        bot.register_next_step_handler(mes, make_way)

@bot.message_handler(commands=['test'])
def send_test(mess):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    bot.send_photo(mess.chat.id, photo=open(f"src/png/{onlyfiles[0]}", 'rb'), caption='Шаг 1', reply_markup=menu1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    if call.message:
        i = re.findall(r'\d', call.message.caption)
        i = int(i[0])
        if call.data == 'left':
            if i != 0:
                i-=1
                try:
                    with open(f'src/png/{onlyfiles[i]}','rb') as f:
                        bot.edit_message_media(telebot.types.InputMediaPhoto(f), call.message.chat.id, call.message.message_id,  reply_markup=menu1)
                        bot.edit_message_caption(f'Шаг: {i}', call.message.chat.id, call.message.message_id, reply_markup=menu1)
                except Exception as e:
                    bot.send_message(call.message.chat.id, f'Ошибка: {e}')
        if call.data == 'right':
                i+=1
                try:
                    with open(f'src/png/{onlyfiles[i]}','rb') as f:
                        bot.edit_message_media( telebot.types.InputMediaPhoto(f), call.message.chat.id, call.message.message_id, call.message.message_id,  reply_markup=menu1)
                        bot.edit_message_caption(f'Шаг: {i}', call.message.chat.id, call.message.message_id, call.message.message_id,  reply_markup=menu1)
                except Exception as e:
                    bot.send_message(call.message.chat.id, f'Ошибка: {e}')


@bot.message_handler(content_types=['text'])
def what_text(mess):
    if mess.text.lower() == 'привет':
        bot.send_message(mess.chat.id, f'Привет, {mess.from_user.first_name}!')
    else:
        bot.send_message(mess.chat.id, 'Я Вас не понимаю')

bot.polling() 