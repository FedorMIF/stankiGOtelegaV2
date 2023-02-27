import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import log
import way
from os import listdir
from os.path import isfile, join

bot = Bot('5240511847:AAEHJgb-EJWnzyvp_JE9kq-wFpwf9q0wZ4c')
dp = Dispatcher(bot, storage=MemoryStorage())

kb = (
        ('<', 'left'), 
        ('>','right')
    )

row_bt = (InlineKeyboardButton(text, callback_data=data) for text, data in kb)

menu1 = InlineKeyboardMarkup(row_width=1)
menu1.row(*row_bt)

class row_auds(StatesGroup):
    numbers = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message):	
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, ')
                                      #f'я бот, который строит маршрут между аудиториями МГТУ Станкин.')

@dp.message_handler(commands=['sendimg'])
async def sen_img(mess):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    await bot.send_photo(mess.chat.id, photo=open(f"src/png/{random.choice(onlyfiles)}.png", 'rb'), caption='Это МТГУ Станкин')

@dp.message_handler(commands=['findway'])
async def what_aud(mess: types.Message, state:FSMContext):
    await bot.send_message(mess.chat.id, 'Напиши *два* номера аудиторий через пробел:\n\n*Аудитория рядом* \t *Аудитория конечная*\n\n_Если хотите отменить команду напишите "Отмена"_', parse_mode="Markdown")
    await state.set_state(row_auds.numbers.state)

@dp.message_handler(state=row_auds.numbers)
async def make_way(mess: types.Message, state:FSMContext):
    await state.update_data(input_auds = mess.text.lower())
    user_data = await state.get_data()
    auds = (user_data['input_auds']).split()
    try:
        num1 = auds[0]
        num2 = auds[1]
        if way.pars_build(num1) and way.pars_build(num2):
            onlyfiles = way.this_is_the_way(auds)
            try:
                await bot.send_photo(mess.chat.id, photo=open(f"src/png/{onlyfiles[0]}.png", 'rb'), caption=f'Путь из {num1} в {num2} \nШаг 1 ', reply_markup=menu1)
            except Exception as e:
                print(e)
            await state.finish()
        else:
            await bot.send_message(mess.chat.id, 'Какого то номера нет, попробуй другой номер')
            await state.set_state(row_auds.numbers.state)
    except:
        if auds[0].lower() == 'отмена':
            await bot.send_message(mess.chat.id, 'Вы решили отменить путешествие по коридорам МТГУ Станкин')
        else:
            await bot.send_message(mess.chat.id, 'Ты ввел не числа, введи просто два номера аудиторий через пробел')
            await state.set_state(row_auds.numbers.state)

@dp.message_handler(commands=['test'])
async def send_test(mess):
    onlyfiles = [f for f in listdir('src/png/') if isfile(join('src/png/', f))]
    await bot.send_photo(mess.chat.id, photo=open(f"src/png/{onlyfiles[0]}.png", 'rb'), caption='Шаг 1', reply_markup=menu1)


@dp.callback_query_handler(text = 'left')
@dp.callback_query_handler(text = 'right')
async def callback_inline(query: types.CallbackQuery):
    nums = (query.message.caption).split()
    onlyfiles = way.this_is_the_way([nums[2], nums[4]])
    i = int(nums[6])
    
    if query.data == 'left':
        if i != 1:
            i-=1
            try:
                with open(f'src/png/{onlyfiles[i-1]}.png','rb') as f:
                    await bot.edit_message_media(types.InputMediaPhoto(f), query.message.chat.id, query.message.message_id,  reply_markup=menu1)
                    await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i}', reply_markup=menu1)
            except Exception as e:
                await log.add(f'{query.message.chat.id} : Ошибка: {e}')
        else:
            await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i} \nНачало маршрута', reply_markup=menu1)
    
    if query.data == 'right':
        if i != len(onlyfiles):
            i+=1
            try:
                with open(f'src/png/{onlyfiles[i-1]}.png','rb') as f:
                    await bot.edit_message_media( types.InputMediaPhoto(f), query.message.chat.id, query.message.message_id,  reply_markup=menu1)
                    await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i}',  reply_markup=menu1)
            except Exception as e:
                await log.add(f'{query.message.chat.id} : Ошибка: {e}')
        else:
            await bot.edit_message_caption(query.message.chat.id, query.message.message_id, caption = f'Путь из {nums[2]} в {nums[4]} \nШаг: {i} \nКонец маршрута', reply_markup=menu1) 


@dp.message_handler(content_types=['text'])
async def what_text(mess):
    if mess.text.lower() == 'привет':
        await bot.send_message(mess.chat.id, f'Привет, {mess.from_user.first_name}!')
    else:
        await bot.send_message(mess.chat.id, 'Я Вас не понимаю')

if __name__ == '__main__':
    executor.start_polling(dp)