import os
from random import randint
import sys
import logging
from typing import Any, Dict
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext



API_TOKEN = '5641212086:AAFAiBv_4r6SeMi6JVAnpnqCsQylkOFf5lw'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    answer_human = State()
    
    
adress = ['answer_hi.txt', 'answer_whats_up.txt', 'answer_weather.txt', 'answer_name.txt','answer_age.txt','answer_time.txt']
bot_answers = {adres : open(mode='r', file = adres, encoding='utf-8').read().split() for adres in adress}
print(bot_answers)
actions = ['-', '+', '*', '/']
counter_false = 0
counter_questions = 0
counter_true = 0
question = ''
game_state = False

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Доступна математическая игра по команде /start_game, а также ответы на эти вопросы:\nПривет\nКак дела?\nКакая погода за окном?\nКак тебя зовут?\nСколько тебе дней?\nКоторый час?")


    
@dp.message_handler(commands=['start_game'])
async def math_game_start(message: types.Message):
    global question, game_state
    actions = ['-', '+', '*', '/']
    await message.answer('Game started, answer the question\nFor stoping game write /stop_game')
    question = f'{randint(1,10)} {actions[randint(0,3)]} {randint(1,10)}'
    await message.answer(question)
    game_state = True
    await Form.answer_human.set()

@dp.message_handler(commands=['stop_game'],state=Form.answer_human)
async def math_game_stop(message: types.Message, state: FSMContext):
    global counter_true, counter_false, counter_false, counter_questions
    await message.answer(f'Number of examples: {counter_questions}\nNumber of correct answers: {counter_true}\nNumber of uncorrect answers: {counter_false}')
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


@dp.message_handler()
async def echo(message: types.Message):
    global bot_answers
    if message.text.lower() == 'привет':
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
        open(mode='r+', file = 'ответы.txt', encoding='utf-8').write(message['from']['username'] + ' ' + message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


