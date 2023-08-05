#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Copyright (c) 2023, Okulus Dev
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
# Импорт стандартных библиотек
import logging

# Импорт сторонних библиотек
from configparser import ConfigParser
from aiogram import Bot, Dispatcher, executor, types

# Импорт локальных файлов
from modules.security.fua import generate_useragent

# Загружаем конфигурационный файл
config = ConfigParser()
config.read('config.ini')

# Создаем константы с важными значениями
ADMIN_ID = config['Telegram']['admin_id']
TOKEN = config['Telegram']['token']
DEV = config['Telegram']['dev']
CHANNEL = config['Telegram']['channel']
BOT_USERNAME = config['Telegram']['bot_username']

# Создание бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
	greeting = f'''Приветствую тебя, {msg.from_user.name}! Я - Punisher, каратель твоих врагов.
Я умею искать информацию, сканировать сайты, и помогать в этичном хакинге!

Вот что я умею:
 + Сканер портов
 + Сканер XSS уязвимостей на сайте
 + Сканер уязвимостей SQL-инъекции на сайте
 + Получение ссылок с сайта
 + Генерация случайного User-Agent
 + Генерация случайного MAC адреса
 + Информация об IP
 + Информация об номере телефона'''
	
	await msg.answer(greeting)


if __name__ == '__main__':
	# Добавляем логгирование
	logging.basicConfig(level=logging.DEBUG, filename='punisher.log', 
						filemode='a', format='%(asctime)s %(levelname)s %(message)s')
	executor.start_polling()
