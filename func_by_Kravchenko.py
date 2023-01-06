from selenium import webdriver
from bs4 import BeautifulSoup
from aiogram import types
import requests
import asyncio
import os
from os import path
from decouple import config
import iso4217
import requests
import json
import datetime
from random import randint
from datetime import time
import time
from aiogram.dispatcher import FSMContext



def update_currency(state = FSMContext):
    json_file = 'currency.json'
    txt_file = 'timeupdate.txt'
    try:
        times = float(open(txt_file, 'r').read())
    except:
        times = 0
        open(txt_file, 'w')
    real_time = time.time()
    if real_time >= times + 300:
        open(txt_file, 'w').write(str(real_time))  
        with open(json_file, "w") as outfile:
            outfile.write(json.dumps(requests.get(f'https://api.monobank.ua/bank/currency').json()))
    with open(json_file, 'r', encoding='utf-8') as f:
        data = f.read()
        b = json.loads(data)
    return b    
        

def inline_keyboard():   
    value_info_keyboard = types.InlineKeyboardMarkup()
    usb_button = types.InlineKeyboardButton('USD', callback_data='USD')
    eur_button = types.InlineKeyboardButton('EUR', callback_data='EUR')
    gbp_button = types.InlineKeyboardButton('GBP', callback_data='GBP')
    again_value_button = types.InlineKeyboardButton('Повторить последний', callback_data='1')
    return value_info_keyboard.add(again_value_button, usb_button, eur_button, gbp_button)

def inline_random():
    list_code = iso4217.get_list_of_currencies()
    keyboard = types.InlineKeyboardMarkup()
    for i in range(3):
        value = list_code[randint(0, len(list_code) - 1)]
        keyboard.add(types.InlineKeyboardButton(value, callback_data=value))
    return keyboard
    
    

def getvaluequery(currency : dict, valuta : any) -> tuple or bool:
    if not valuta.isdigit():
        try:
            code = iso4217.get_currency(valuta).num
        except:
            return False
    else:
        code = int(valuta)
    for i in currency:
        if i['currencyCodeA'] == code:
            if i['rateBuy']:
                return i['rateBuy'], i['rateSell']
            else: 
                return i['rateCross'], i['rateCross'] * 1.0215
    return False

API_TOKEN_WEATHER = config('WEATHER_API_TOKEN')

# item_list = []
# b = requests.get(url='https://fortnite-api.com/v2/shop/br/combined',headers= {'Authorization' : API_TOKEN}).json()
# with open('combined(1).json', 'r', encoding='utf-8') as f:
#     data = f.read()
#     b = json.loads(data)
# for i in range(len(b['data']['featured']['entries'])):
#     item_list.append(b['data']['featured']['entries'][i]\
        # ['items'][0]['name'])#все предметы кроме дайли
# print(b['data']['daily']['entries'][0]['items'])# daily items
# print(b['data']['featured']['entries'][0]['bundle']['name'])#bundles
# dict_1 = {}
# for i in range(90):
#     if b['data']['featured']['entries'][i]['bundle']:
#         namess = b['data']['featured']['entries'][i]['bundle']['name']
#     else:
#         namess = b['data']['featured']['entries'][i]['items'][0]['name']
#     pricess = b['data']['featured']['entries'][i]['finalPrice']
#     dict_1[namess] = pricess
# # print(dict_1)
# print(dict_1)
    
def reverse_str(text, first_char, second_char):
    return text[len(text) - second_char - 2 : first_char : -1]


def sub_string(str_1 : str) -> bool:
    len_str = len(str_1)
    sub_str = str_1[0]
    result = False
    if len_str == 1:
        pass       
    elif str_1.count(sub_str) == len_str:
            result = True
    else:        
        a = 1
        for i in range(1, len_str // 2):
            sub_str = sub_str + str_1[i]
            a += 1
            counter = str_1.count(sub_str)
            if counter == len_str / a:
                result = True
                break
    return result



def getimage(var):
    if not path.exists('image'):
        os.mkdir('image')
    else:
        if path.exists(f'image/{var}.txt'):
            return
        
    scrollnum = 1
    sleepTimer = 1
    url=f'https://ru.pinterest.com/search/pins/?q={var}&rs=typed'
    


    driver=webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, 'html.parser')

    i = 0
    list_links = []
    for link in soup.findAll('img'):   
        if i == 6:
            break
        namesimage = link.get('src')
        list_links.append(namesimage + '\n')
        i += 1
    open(mode='w', file =f'image/{var}.txt', encoding='utf-8').write(''.join(list_links))
    return list_links

def getweather(city : str) -> tuple:
    main = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_TOKEN_WEATHER}&lang=ua').json()
    return main.get('weather')[0].get('description'), str(main.get('main').get('temp'))



