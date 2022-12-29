import os
import sys
import logging
import asyncio

from random import randint
from typing import Any, Dict
from func_by_Kravchenko import getimage, sub_string, getweather
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from decouple import config


API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    answer_bot = State()
    answer_human = State()
    sub_string_form = State()
      
class Weather(StatesGroup):
    start = State()
    location = State()
    viev = State()

adress = ['answer_hi.txt','answer_whats_up.txt', 'answer_weather.txt','answer_name.txt','answer_age.txt','answer_time.txt']
bot_answers = {adres : open(mode='r', file = adres, encoding='utf-8').read().split() for adres in adress}
if not os.path.exists('image'):
        os.mkdir('image')
bot_images = {adres : open(mode='r', file = f'image/{adres}', encoding='utf-8').read().split() for adres in os.listdir(path='image')}
actions = ['-', '+', '*', '/']
counter_false = 0
counter_questions = 0
counter_true = 0
question = ''


main_keyboard = types.ReplyKeyboardMarkup()
math_game_start_keyboard = types.InlineKeyboardMarkup()
math_game_answers_keyboard = types.InlineKeyboardMarkup()
math_game_stop_keyboard = types.ReplyKeyboardMarkup()
sub_string_keyboaed = types.ReplyKeyboardMarkup()
weather_info_keyboard = types.ReplyKeyboardMarkup()
weather_start_keyboard = types.InlineKeyboardMarkup()
weather_end_keyboard = types.InlineKeyboardMarkup()

start_button = types.KeyboardButton('/start')
start_game_button = types.KeyboardButton('/start_game')
start_sub_string_button = types.KeyboardButton('/start_sub_string')
start_weather_info_button = types.KeyboardButton('/start_weather_info')
stop_weather_info_button = types.KeyboardButton('/stop_weather_info')
math_game_stop_button = types.KeyboardButton('/stop_game')
sub_string_button = types.KeyboardButton('/stop_sub_string')
type_game_1 = types.InlineKeyboardButton('Выбор решения', callback_data='type_1')
type_game_2 = types.InlineKeyboardButton('Вписывание ответа', callback_data='type_2')
dnipro_city = types.InlineKeyboardButton('Дніпро', callback_data='Dnipro')
kiev_city = types.InlineKeyboardButton('Київ', callback_data='Kiev')
tours_city = types.InlineKeyboardButton('Тур', callback_data='Tours')
again_city = types.InlineKeyboardButton('Новый город', callback_data='1')
new_city = types.InlineKeyboardButton('Повторить погоду', callback_data='0')

main_keyboard.add(start_game_button, start_sub_string_button, start_weather_info_button)
math_game_start_keyboard.add(type_game_1, type_game_2)
math_game_stop_keyboard.add(math_game_stop_button)
sub_string_keyboaed.add(sub_string_button)
weather_info_keyboard.add(stop_weather_info_button, start_button)
weather_start_keyboard.add(dnipro_city, kiev_city, tours_city)
weather_end_keyboard.add(new_city, again_city)

"        Основное     "
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет!\nЯ бот Аби)\nПо команде /help - перечень функция', reply_markup=main_keyboard)#

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Доступны функции:\nМатематическая игра по команде /start_game\nСожержится ли подстрока в строке /start_sub_string\nПри просьбе дать картинку\n(Например:Привет, кинь, пж, картинку кота)\nотправляет картинку\n(если хотите найти картинку по нескольким словам напишите их через подчеркивание)\n(Картинка ищется через pinterest, иногда может не совпадать с темой)\nИнформация по погоде /start_weather_info\nОтветы на эти вопросы:\nПривет\nКак дела?\nКакая погода за окном?\nКак тебя зовут?\nСколько тебе дней?\nКоторый час?",)
    
        
 
"       Математическая игра          "   
@dp.message_handler(commands=['start_game'])
async def math_game_start(message: types.Message):
    await message.reply('Выберете режим игры', reply_markup=math_game_start_keyboard)
    await Form.answer_bot.set()     
    
@dp.callback_query_handler(state=Form.answer_bot)
async def inline_buttons(query: types.CallbackQuery):
    global question
    actions = ['-', '+', '*', '/']  
    if query.data == 'type_1':
        false_question = ''
        number_question = randint(0,3)
        question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
        math_game_answers_keyboard = types.InlineKeyboardMarkup()
        for i in range(4):
            if i == number_question:
                math_game_answers_keyboard.add(types.InlineKeyboardButton(question, callback_data='True'))
            else:
                while True:
                    false_question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
                    if eval(false_question) != eval(question):
                        math_game_answers_keyboard.add(types.InlineKeyboardButton(text = false_question, callback_data='False'))
                        break
        await query.message.answer('Game started, answer the question\nFor stoping game write /stop_game', reply_markup=math_game_stop_keyboard)
        await query.message.answer(eval(question),reply_markup=math_game_answers_keyboard)
        await Form.answer_human.set()
    elif query.data == 'type_2':        
        await query.message.answer('Game started, answer the question\nFor stoping game write /stop_game', reply_markup=math_game_stop_keyboard)
        question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
        await query.message.answer(question)
        await Form.answer_human.set()
            
@dp.message_handler(commands=['stop_game'],state=Form.answer_human)
async def math_game_stop(message: types.Message, state: FSMContext):
    global counter_true, counter_false, counter_false, counter_questions
    await message.answer(f'Number of examples: {counter_questions}\nNumber of correct answers: {counter_true}\nNumber of uncorrect answers: {counter_false}', reply_markup=main_keyboard)
    if counter_true > counter_false:
        await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGv01jkxdn7vbKlIxKhtKhBYUYUNcZoQACCgADnP4yMFsQVnkk-4rwKwQ')
    elif counter_true < counter_false:
        await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGv09jkxd9GOk0JuebctwhJ4q28uBtJQACGAADnP4yMJPRPDIBxPOGKwQ')
    else:
        await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGwhljlFHGRmk1awEWbJC4e7ENLx-6JgACCwADnP4yMPctMM3hxWgtKwQ')
    counter_false = 0
    counter_questions = 0
    counter_true = 0
    await state.finish()
           
@dp.callback_query_handler(state=Form.answer_human)
async def inline_buttons_game(query: types.CallbackQuery):
    global question, counter_true, counter_false, counter_false, counter_questions
    if query.data == 'True':
        counter_true += 1
        answer_ = 'Yes, next question:\n'
        counter_questions += 1
        number_question = randint(0,3)
    else:
        counter_false += 1
        answer_ = f'Wrong, {question}, next question:\n'
        counter_questions += 1
    number_question = randint(0,3)
    question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
    math_game_answers_keyboard = types.InlineKeyboardMarkup()
    for i in range(4):
        if i == number_question:
            math_game_answers_keyboard.add(types.InlineKeyboardButton(question, callback_data='True'))
        else:
            while True:
                false_question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
                if eval(false_question) != eval(question):
                    math_game_answers_keyboard.add(types.InlineKeyboardButton(text = false_question, callback_data='False'))
                    break
    await query.message.answer(answer_ + str(eval(question)), reply_markup=math_game_answers_keyboard)

@dp.message_handler(state=Form.answer_human)
async def math_game_counter(message: types.Message, state: FSMContext):
    global question, counter_true, counter_false, counter_false, counter_questions
    human_anwer = message.text
    actions = ['-', '+', '*', '/']
    if human_anwer == str(int(eval(question))):
        counter_true += 1
        answer_ = 'Yes, next question:\n'
    else: 
        counter_false += 1
        answer_ = f'Wrong, {str(int(eval(question)))}, next question:\n'
    counter_questions += 1
    question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
    await message.answer(answer_ + question)
    
    
    
    
"          Подстроки              "
@dp.message_handler(commands=['start_sub_string'])
async def sub_string_start(message: types.Message):
    await message.reply('Sub string detection is started', reply_markup=sub_string_keyboaed)
    await Form.sub_string_form.set()

@dp.message_handler(commands=['stop_sub_string'],state=Form.sub_string_form)
async def sub_string_stop(message: types.Message, state: FSMContext):
    await message.reply('Sub string detection is stoped', reply_markup=main_keyboard)
    await state.finish()

@dp.message_handler(state=Form.sub_string_form)
async def sub_string_main(message: types.Message, state: FSMContext):
    await message.reply(sub_string(message.text))




"               Погода              "
@dp.message_handler(commands=['start_weather_info'])
async def weather_info_startt(message: types.Message):
    await message.reply('Вітаю у меню інформації о погоді!\nВведіть /start',reply_markup=weather_info_keyboard)
    await Weather.start.set()
    
@dp.message_handler(commands=['stop_weather_info'], state=(Weather.start, Weather.location, Weather.viev))
async def weather_info_stop(message: types.Message, state: FSMContext):
    await message.reply('Weather info is stoped', reply_markup=main_keyboard)
    await state.finish()
       
@dp.message_handler(commands=['start'], state=Weather.start)
async def weather_infoe_start(message: types.Message):
    await message.answer('Оберіть місто в якому цікавить погода:', reply_markup=weather_start_keyboard)
    await Weather.location.set()

@dp.callback_query_handler(state=Weather.location)
async def weather_info_location(query: types.CallbackQuery, state: FSMContext):
    city_dict = {'Dnipro' : 'Дніпро', 'Kiev' : 'Київ', 'Tours' : 'Тур'}
    weather_city = getweather(query.data)
    answer_weather = f'У місті {city_dict[query.data]} {weather_city[0]}, температура {weather_city[1]}°C'
    await query.message.edit_text(answer_weather, reply_markup=weather_start_keyboard)
    async with state.proxy() as data:
        data['answer'] = answer_weather

@dp.message_handler(commands=['start'], state=(Weather.location, Weather.viev))
async def weather_info_end(message: types.Message):
    await message.reply('Оберіть що ви хочете зробити:', reply_markup=weather_end_keyboard)
    await Weather.viev.set()
    
@dp.callback_query_handler(state=Weather.viev)
async def weather_end(query: types.CallbackQuery, state: FSMContext):
    if query.data == '1':
        await query.message.edit_text('Оберіть місто в якому цікавить погода:',reply_markup=weather_start_keyboard)
        await Weather.location.set()
    elif query.data == '0':
        async with state.proxy() as data:
            await query.message.edit_text(data['answer'], reply_markup= types.InlineKeyboardMarkup().add(again_city))
    
            

    



@dp.message_handler()
async def echo(message: types.Message):
    global bot_answers, bot_images
    index_var = 0
    messege_text= message.text.lower().split()
    if 'картинк' in message.text.lower():
        for i in messege_text:
            index_var +=1
            if 'картинк' in i:
                break
        image_pic = messege_text[index_var]
        image_pic_txt = f'{image_pic}.txt'
        try:
            bot_images[image_pic_txt]
        except:
            bot_images[image_pic_txt] = getimage(image_pic)
        try:
            await bot.send_photo(message.chat.id, bot_images[image_pic_txt][randint(0,len(bot_images[image_pic_txt])-1)])      
        except:
             await message.reply('Картинки по запросу не нашлось(')       
    elif message.text.lower() == 'привет':
        await message.answer(bot_answers['answer_hi.txt'][randint(0,len(bot_answers['answer_hi.txt']) - 1)])
    elif message.text.lower() == 'как дела?':
        await message.answer(bot_answers['answer_whats_up.txt'][randint(0,len(bot_answers['answer_whats_up.txt']) - 1)])
    elif message.text.lower() == 'какая погода за окном?':
        await message.answer(bot_answers['answer_weather.txt'][randint(0,len(bot_answers['answer_weather.txt']) - 1)])
    elif message.text.lower() == 'как тебя зовут?':
        await message.answer(bot_answers['answer_name.txt'][randint(0,len(bot_answers['answer_name.txt']) - 1)])
    elif message.text.lower() == 'сколько тебе дней?':
        await message.answer(bot_answers['answer_age.txt'][randint(0,len(bot_answers['answer_age.txt']) - 1)])
    elif message.text.lower() == 'который час?':
        await message.answer(bot_answers['answer_time.txt'][randint(0,len(bot_answers['answer_time.txt']) - 1)])
    else:
        await message.answer(message.text)
        # open(mode='r+', file = 'ответы.txt', encoding='utf-8').write(f'{message.from} : {message.text}\n')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    


