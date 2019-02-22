# -*- coding: utf-8 -*-
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''


from sys import argv
import pprint
import re


def parse_sh_ip_int_br(filename):
	with open(filename, 'r') as f:
		content = f.read()
		regex = re.compile(r'(\S+)\s+(unassigned|\d+\.\d+\.\d+\.\d+)\s+.+((?:administratively )+down|up)\s+(up|down)')
	return regex.findall(content)


if __name__ == '__main__':
	pprint.pprint(parse_sh_ip_int_br(argv[1]))

