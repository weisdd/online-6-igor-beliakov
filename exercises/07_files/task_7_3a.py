# -*- coding: utf-8 -*-
'''
Задание 7.3a

Сделать копию скрипта задания 7.3.

Дополнить скрипт:
- Отсортировать вывод по номеру VLAN

В результате должен получиться такой вывод:
10       01ab.c5d0.70d0      Gi0/8
10       0a1b.1c80.7000      Gi0/4
100      01bb.c580.7000      Gi0/1
200      0a4b.c380.7c00      Gi0/2
200      1a4b.c580.7000      Gi0/6
300      0a1b.5c80.70f0      Gi0/7
300      a2ab.c5a0.700e      Gi0/3
500      02b1.3c80.7b00      Gi0/5
1000     0a4b.c380.7d00      Gi0/9


Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

# В решении допускается, что в одном VLAN может быть несколько портов с несколькими MAC-адресами
cam_table = {}

with open('CAM_table.txt') as f:
	for line in f:
		# Исключаем пустые строки и строки, начинающиеся не с числа
		if line.strip() == '' or not line.split()[0].isdigit(): continue
		vlan_id, mac, _, port = line.split()
		cam_table.setdefault(vlan_id, {})
		cam_table[vlan_id].setdefault(port, [])
		cam_table[vlan_id][port].append(mac)

for vlan_id in sorted(cam_table, key=int):
	for port in cam_table[vlan_id]:
		for mac in cam_table[vlan_id][port]:
			print('{}\t{}\t{}'.format(vlan_id, mac, port))
