# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):
	access = {}
	trunk = {}
	result = (access, trunk)
	with open(config_filename, 'r') as f:
		interface = mode = ''
		vlans = 1
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
				interface = mode = ''
				vlans = 1
	return result


