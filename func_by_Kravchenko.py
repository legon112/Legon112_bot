from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time 
import os
import shutil
from os import path

def reverse_str(text, first_char, second_char):
    return text[len(text) - second_char - 2 : first_char : -1]


def getimage(var):
    if not path.exists('image'):
        os.mkdir('image')
    else:
        if path.exists(f'image/{var}.txt'):
            return
        
    scrollnum = 1
    sleepTimer = 1
    # url=f'https://ru.pinterest.com/search/pins/?q={var}'
    url=f'https://ru.pinterest.com/search/pins/?q={var}&rs=typed'
    


    options=webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["enable-logging"])
    driver=webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.get(url)
    for i in range(1,scrollnum): 
        driver.execute_script("window.scrollTo(1,100000)") 
        print('scroll-down')
        time.sleep(sleepTimer)
    soup=BeautifulSoup(driver.page_source, 'html.parser')

    it = 0
    list_links = []
    for link in soup.findAll('img'):   
        if it == 6:
            break
        namesimage = link.get('src')
        list_links.append(namesimage + '\n')
        it += 1
    open(mode='w', file =f'image/{var}.txt', encoding='utf-8').write(''.join(list_links))
    return list_links
