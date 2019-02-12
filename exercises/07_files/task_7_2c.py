# -*- coding: utf-8 -*-
'''
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

_, filename_source, filename_destination = argv

with open(filename_source, 'r') as f_s, open(filename_destination, 'w') as f_d:
	for line in f_s:
		ignore_flag = 0
		for pattern in ignore:
			if pattern in line:
				ignore_flag = 1
				break
		if not ignore_flag: f_d.write(line)
