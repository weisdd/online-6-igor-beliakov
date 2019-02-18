# -*- coding: utf-8 -*-
'''
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов, а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
'''

import re
import pprint
from sys import argv

def generate_description_from_cdp(filename):
	regex = r'^(?P<hostname>\S+)\s+(?P<local_interface>\S+ \S+)\s+\d+\s+.+?(?P<remote_interface>\S+ \S+)$'
	result = {}
	with open(filename, 'r') as f:
		content = f.read()
		for match in re.finditer(regex, content, re.MULTILINE):
			hostname, local_interface, remote_interface = match.group('hostname', 'local_interface', 'remote_interface')
			result[local_interface] = f'description Connected to {hostname} port {remote_interface}'
	return result


if __name__ == '__main__':
	pprint.pprint(generate_description_from_cdp(argv[1]))
	
