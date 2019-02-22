# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''

import re
from sys import argv

def get_ints_without_description(filename):
	regex = r'^(interface (\S+)\n.+?)!' # full config for an interface
	result = []
	with open(filename, 'r') as f:
		content = f.read()
		for match in re.finditer(regex, content, re.DOTALL|re.MULTILINE):
			if 'description' not in match.group(1):
				result.append(match.group(2))
	return result


if __name__ == '__main__':
	print(get_ints_without_description(argv[1]))

# Все отлично

