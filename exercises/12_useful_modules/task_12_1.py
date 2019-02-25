# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

import subprocess

def ping_ip_addresses(ips):
	result_alive = []
	result_dead = []
	for ip in ips:
		command_output = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, encoding='utf-8')
		if command_output.returncode == 0:
			result_alive.append(ip)
		else:
			result_dead.append(ip)
	return result_alive, result_dead


def main():
	print(ping_ip_addresses(['8.8.8.8', '8.8.8.9', '8.8.8.10', '8.8.4.4']))


if __name__ == '__main__':
	main()

# Все отлично
