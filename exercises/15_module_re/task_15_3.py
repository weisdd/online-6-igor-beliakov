# -*- coding: utf-8 -*-
'''
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
'''


import re
from sys import argv


def convert_ios_nat_to_asa(src_file, dst_file):
	regex = r'ip nat inside source static tcp (\S+) (\d+) interface \S+ (\d+)'
	template = ('object network LOCAL_{ip}\n'
				' host {ip}\n'
				' nat (inside,outside) static interface service tcp {src_port} {dst_port}\n')
	with open(src_file, 'r') as s_f, open(dst_file, 'w') as d_f:
		content = s_f.read()
		for match in re.finditer(regex, content):
			ip, src_port, dst_port = match.groups()
			d_f.write(template.format(ip = ip, src_port = src_port, dst_port = dst_port))
	return None


if __name__ == '__main__':
	convert_ios_nat_to_asa(argv[1], argv[2])

# Все отлично

# вариант решения
def convert_ios_nat_to_asa(cisco_ios, cisco_asa):
    regex = ('source static tcp (?P<local_ip>\S+) +'
             '(?P<lport>\d+) +interface +\S+ (?P<outside_port>\d+)')
    asa_template = ('object network LOCAL_{local_ip}\n'
                    ' host {local_ip}\n'
                    ' nat (inside,outside) static interface service tcp {lport} {outside_port}\n')
    with open(cisco_ios) as f, open(cisco_asa, 'w') as asa_nat_cfg:
        for match in re.finditer(regex, f.read()):
            asa_nat_cfg.write(asa_template.format(**match.groupdict()))

if __name__ == '__main__':
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'cisco_asa_config.txt')
