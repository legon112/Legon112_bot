import os
from random import randint

def spliting(adress):
    return open(mode='r', file = adress, encoding='utf-8').read().split()

"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5641212086:AAFAiBv_4r6SeMi6JVAnpnqCsQylkOFf5lw'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Доступны ответы на эти вопросы:\nПривет\nКак дела?\nКакая погода за окном?\nКак тебя зовут?\nСколько тебе дней?\nКоторый час?")



@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    if message.text == 'Привет':
        await message.answer(spliting('answer_hi.txt')[randint(0,len(spliting('answer_hi.txt')) - 1)])
    elif message.text == 'Как дела?':
        await message.answer(spliting('answer_whats_up.txt')[randint(0,len(spliting('answer_whats_up.txt')) - 1)])
    elif message.text == 'Какая погода за окном?':
        await message.answer(spliting('answer_weather.txt')[randint(0,len(spliting('answer_weather.txt')) - 1)])
    elif message.text == 'Как тебя зовут?':
        await message.answer(spliting('answer_name.txt')[randint(0,len(spliting('answer_name.txt')) - 1)])
    elif message.text == 'Сколько тебе дней?':
        await message.answer(spliting('answer_age.txt')[randint(0,len(spliting('answer_age.txt')) - 1)])
    elif message.text == 'Который час?':
        await message.answer(spliting('answer_time.txt')[randint(0,len(spliting('answer_time.txt')) - 1)])
    else:
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



