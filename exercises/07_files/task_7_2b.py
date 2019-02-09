# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

filename_source = argv[1]
filename_destination = 'config_sw1_cleared.txt'

with open(filename_source, 'r') as f_s, open(filename_destination, 'w') as f_d:
	for line in f_s:
		ignore_flag = 0
		for pattern in ignore:
			if pattern in line:
				ignore_flag = 1
				break
		if not ignore_flag: f_d.write(line)
