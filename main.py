import os
import sys
import logging
import asyncio

from random import randint
from typing import Any, Dict
from func_by_Kravchenko import getimage, sub_string
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
    answer_human = State()
    sub_string_form = State()

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
start_game_button = types.KeyboardButton('/start_game')
start_sub_string_button = types.KeyboardButton('/start_sub_string')
math_game_stop_button = types.KeyboardButton('/stop_game')
sub_string_button = types.KeyboardButton('/start_sub_string')
type_game_1 = types.InlineKeyboardButton('Выбор решения', callback_data='type_1')
type_game_2 = types.InlineKeyboardButton('Вписывание ответа', callback_data='type_2')
main_keyboard.add(start_game_button, start_sub_string_button)
math_game_start_keyboard.add(type_game_1, type_game_2)
math_game_stop_keyboard.add(math_game_stop_button)
sub_string_keyboaed.add(sub_string_button)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет!\nЯ бот Аби)\nПо команде /help - перечень функция') #, reply_markup=main_keyboard

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Доступны функции:\nМатематическая игра по команде /start_game\nСожержится ли подстрока в строке /start_sub_string\nПри просьбе дать картинку\n(Например:Привет, кинь, пж, картинку кота)\nотправляет картинку\n(если хотите найти картинку по нескольким словам напишите их через подчеркивание)\n(Картинка ищется через pinterest, иногда может не совпадать с темой)\nОтветы на эти вопросы:\nПривет\nКак дела?\nКакая погода за окном?\nКак тебя зовут?\nСколько тебе дней?\nКоторый час?",)
    
    
    
    
@dp.message_handler(commands=['start_game'])
async def math_game_start(message: types.Message):
    await message.reply('Выберете режим игры', reply_markup=math_game_start_keyboard)
    
    

    
@dp.callback_query_handler()
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
    

@dp.message_handler(commands=['stop_game'],state=Form.answer_human)
async def math_game_stop(message: types.Message, state: FSMContext):
    global counter_true, counter_false, counter_false, counter_questions
    await message.answer(f'Number of examples: {counter_questions}\nNumber of correct answers: {counter_true}\nNumber of uncorrect answers: {counter_false}', reply_markup=types.ReplyKeyboardRemove())
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
    
    
    
    
    
@dp.message_handler(commands=['start_sub_string'])
async def math_game_start(message: types.Message):
    await message.reply('Sub string detection is started', reply_markup=sub_string_keyboaed)
    await Form.sub_string_form.set()

@dp.message_handler(commands=['stop_sub_string'],state=Form.sub_string_form)
async def math_game_stop(message: types.Message, state: FSMContext):
    await message.reply('Sub string detection is stoped',reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(state=Form.sub_string_form)
async def math_game_counter(message: types.Message, state: FSMContext):
    await message.reply(sub_string(message.text))





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
        # open(mode='r+', file = 'ответы.txt', encoding='utf-8').write(f'{message.from}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    


