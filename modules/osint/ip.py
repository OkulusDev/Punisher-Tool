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
import os
import requests
import socket


def get_ip(hostname):
	try:
		ip = socket.gethostbyname(hostname)
		return ip
	except Exception as e:
		return f"[!] Произошла ошибка: {e}"


def get_server_name(hostname, fua):
	try:
		headers = {
			'User-Agent': fua
		}
		content = requests.get(hostname, headers=headers)
		server = content.headers['Server']

		return server
	except Exception as e:
		return "[!] Произошла ошибка: {e}"


def get_info_about_ip(ipaddr, fua):
	content = ''

	try:
		headers = {
			'User-Agent': fua
		}
		info_data = requests.get(f'https://ipinfo.io/{ipaddr}/json', headers=headers).json()
	except Exception as ex:
		content = f'Ошибка: {ex}'
		return content

	whois_info = os.popen(f'whois {ipaddr}').read().strip()

	print(f'IP: {info_data.get("ip")}')
	print(f'Город: {info_data.get("city")}')
	print(f'Регион: {info_data.get("region")}')
	print(f'Страна: {info_data.get("country")}')
	print(f'Имя хоста: {info_data.get("hostname")}')
	print(f'JSON данные: {info_data}')

	content = f'''Информация об IP {ipaddr}
IP: {info_data.get("ip")}
Город: {info_data.get("city")}
Регион: {info_data.get("region")}
Страна: {info_data.get("country")}
Имя хоста: {info_data.get("hostname")}
JSON данные: {info_data}

WhoIs:
{whois_info}
	'''

	return content
