# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

from sys import argv

filename = argv[1]

with open(filename, 'r') as f:
	for line in f:
		if line.startswith('!'):
			continue
		ignore_flag = 0
		for pattern in ignore:
			if pattern in line:
				ignore_flag = 1
				break
		if not ignore_flag:
			print(line, end='')

#Все отлично

#вариант решения
with open(filename) as f:
    for line in f:
        skip_line = False
        for ignore_word in ignore:
            if ignore_word in line:
                skip_line = True
                break
        if not line.startswith('!') and not skip_line:
            print(line.rstrip())


#Вариант с генератором списка
with open(filename) as f:
    for line in f:
        ignore_line = True in [word in line for word in ignore]
        if not line.startswith('!') and not ignore_line:
            print(line.rstrip())
