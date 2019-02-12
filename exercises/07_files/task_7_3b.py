# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

cam_table = {}

with open('CAM_table.txt') as f:
	for line in f:
		# Исключаем пустые строки и строки, начинающиеся не с числа
		if line.strip() == '' or not line.split()[0].isdigit(): continue
		vlan_id, mac, _, port = line.split()
		cam_table.setdefault(vlan_id, {})
		cam_table[vlan_id].setdefault(port, [])
		cam_table[vlan_id][port].append(mac)


vlan_id = input('Введите номер VLAN: ').strip()

if vlan_id in cam_table:
	for port in cam_table[vlan_id]:
		for mac in cam_table[vlan_id][port]:
			print('{}\t{}\t{}'.format(vlan_id, mac, port))
else:
	print('Такого VLAN нет в базе')
