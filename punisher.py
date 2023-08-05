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
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Импорт локальных файлов
from modules.security.fua import generate_useragent
from modules.scanners.url_validator import check_string
from modules.scanners.xss import scan_xss
from modules.scanners.sql_injection import scanning
from modules.osint.ip import get_info_about_ip
from modules.osint.phone import get_info_phonenumber
from keyboards import get_admin_keyboard
# from database import Database; TODO: Сделать базу данных

# Загружаем конфигурационный файл
config = ConfigParser()
config.read('config.ini')

# Создаем константы с важными значениями
ADMINS = config['Telegram']['admins'].split(' ')
print(ADMINS)
TOKEN = config['Telegram']['token']
CHANNEL = config['Telegram']['channel']
BOT_USERNAME = config['Telegram']['bot_username']

# Создание бота и диспетчера
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class ScanXSS(StatesGroup):
	url = State()


class ScanSQLINJ(StatesGroup):
	url = State()


class GetInfoAboutIP(StatesGroup):
	ipaddr = State()


class PhoneInfo(StatesGroup):
	phonenum = State()


@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
	if str(msg.from_user.id) in ADMINS:
		is_admin = True
		print('a')
	else:
		is_admin = False
		print('b')
	greeting = f'''Приветствую тебя! Я - <b>Punisher ToolKit</b>, каратель твоих врагов.
Я умею искать информацию, сканировать сайты, и помогать в этичном хакинге!

Вот что я умею:
<i> + Сканер портов</i>
<i> + Сканер XSS уязвимостей на сайте: /scan_xss</i>
<i> + Сканер уязвимостей SQL-инъекции на сайте: /scan_sqlinj</i>
<i> + Получение ссылок с сайта</i>
<i> + Генерация случайного User-Agent: /fake_useragent</i>
<i> + Генерация случайного MAC адреса</i>
<i> + Информация об IP: /ip</i>
<i> + Информация об номере телефона: /phone</i>'''
	
	await bot.send_message(msg.from_user.id, greeting, parse_mode='html')

	if is_admin:
		await bot.send_message(msg.from_user.id, 'Приветствую, администратор!', 
								reply_markup=get_admin_keyboard())


@dp.message_handler(commands=['phone'])
async def get_info_phone_handler(msg: types.Message):
	await PhoneInfo.phonenum.set()
	await bot.send_message(msg.from_user.id, 'Отправьте номер телефона')


@dp.message_handler(state=PhoneInfo.phonenum)
async def start_get_info_phone_handler(msg: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['phonenum'] = msg.text

	await bot.send_message(msg.from_user.id, 'Подождите...')

	result = get_info_phonenumber(msg.text, generate_useragent())

	await bot.send_message(msg.from_user.id, result)

	await state.finish()


@dp.message_handler(commands=['ip'])
async def get_info_ip_handler(msg: types.Message):
	await GetInfoAboutIP.ipaddr.set()
	await bot.send_message(msg.from_user.id, 'Отправьте IP адрес')


@dp.message_handler(state=GetInfoAboutIP.ipaddr)
async def start_get_info_ip_handler(msg: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['ipaddr'] = msg.text

	await bot.send_message(msg.from_user.id, 'Подождите...')

	result = get_info_about_ip(msg.text, generate_useragent())

	await bot.send_message(msg.from_user.id, f'{result}', parse_mode='html')

	await state.finish()


@dp.message_handler(commands=['scan_xss'])
async def scan_xss_handler(msg: types.Message):
	await ScanXSS.url.set()
	await bot.send_message(msg.from_user.id, 'Отправьте ссылку на сайт')


@dp.message_handler(state=ScanXSS.url)
async def start_scanning_xss_handler(msg: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['url'] = msg.text

	if check_string(msg.text):
		await bot.send_message(msg.from_user.id, 'Подождите...')

		results = scan_xss(msg.text, generate_useragent())

		await bot.send_message(msg.from_user.id, f'Уязвимость: {results[0]}')

		for result in results[1]:
			await bot.send_message(msg.from_user.id, result, parse_mode='HTML')
	else:
		await bot.send_message(msg.from_user.id, 'Вы ввели не ссылку')

	await state.finish()


@dp.message_handler(commands=['scan_sqlinj'])
async def scan_sqlinj_handler(msg: types.Message):
	await ScanSQLINJ.url.set()
	await bot.send_message(msg.from_user.id, 'Отправьте ссылку на сайт')


@dp.message_handler(state=ScanSQLINJ.url)
async def start_scanning_sqlinj_handler(msg: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['url'] = msg.text

	if check_string(msg.text):
		await bot.send_message(msg.from_user.id, 'Подождите...')

		results = scanning(generate_useragent(), msg.text)

		for result in results:
			await bot.send_message(msg.from_user.id, result, parse_mode='HTML')
	else:
		await bot.send_message(msg.from_user.id, 'Вы ввели не ссылку')

	await state.finish()


@dp.message_handler(commands=['fake_useragent'])
async def fakeua_handler(msg: types.Message):
	await bot.send_message(msg.from_user.id, f'Случайный фейковый User-Agent: {generate_useragent()}')


@dp.message_handler()
async def echo(msg: types.Message):
	if msg.text == 'Добавить пользователя':
		...
	elif msg.text == 'Удалить пользователя':
		...
	elif msg.text == 'Скрыть данные пользователя':
		...
	elif msg.text == 'Добавить БД для поиска':
		...
	else:
		await bot.send_message(msg.from_user.id, f'Команда "{msg.text}" не найдена')


async def on_startup(_):
	print(f'{BOT_USERNAME} был запущен!')


if __name__ == '__main__':
	# Добавляем логгирование
	#logging.basicConfig(level=logging.INFO, filename='punisher.log', 
	#					filemode='a', format='[%(levelname)s] [%(asctime)s] %(message)s\n')
	

	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
