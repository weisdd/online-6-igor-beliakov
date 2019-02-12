# -*- coding: utf-8 -*-
'''
Задание 7.3

Скрипт должен обрабатывать записи в файле CAM_table.txt.
Каждая строка, где есть MAC-адрес, должна быть обработана таким образом,
 чтобы на стандартный поток вывода была выведена таблица вида (показаны не все строки из файла):

 100    01bb.c580.7000   Gi0/1
 200    0a4b.c380.7000   Gi0/2
 300    a2ab.c5a0.7000   Gi0/3
 100    0a1b.1c80.7000   Gi0/4
 500    02b1.3c80.7000   Gi0/5
 200    1a4b.c580.7000   Gi0/6
 300    0a1b.5c80.7000   Gi0/7

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

with open('CAM_table.txt') as f:
	for line in f:
		if line.strip() == '' or not line.split()[0].isdigit(): continue
		vlan_id, mac, _, port = line.split()
		print('{}\t{}\t{}'.format(vlan_id, mac, port))

#Все отлично

#вариант решения
with open('CAM_table.txt', 'r') as conf:
    for line in conf:
        line = line.split()
        if line and line[0].isdigit():
            vlan, mac, _, interface = line
            print('{:9}{:20}{}'.format(vlan, mac, interface))

