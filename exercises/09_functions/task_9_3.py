# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):
	access = {}
	trunk = {}
	result = (access, trunk)
	with open(config_filename, 'r') as f:
		interface = mode = vlans = ''
		for line in f:
			if line.startswith('interface'):
				interface = line.split()[1]
			elif line.strip().startswith('switchport mode'):
				mode = line.split()[-1]
			elif 'allowed vlan' in line or 'access vlan' in line:
				vlans = line.split()[-1]
			if line.startswith('!') and interface and mode and vlans:
				if mode == 'access':
					access[interface] = int(vlans)
				elif mode == 'trunk':
					trunk[interface] = [int(vlan) for vlan in vlans.split(',')]
				interface = mode = vlans = ''
	return result


