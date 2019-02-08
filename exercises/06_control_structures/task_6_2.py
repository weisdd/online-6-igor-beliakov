# -*- coding: utf-8 -*-
'''
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить тип IP-адреса.
3. В зависимости от типа адреса, вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-127
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ip = input('Введите IP-адрес: ').strip()
first_byte = int(ip[:ip.index('.')])

if first_byte in range(1,128):
	print('unicast')
elif first_byte in range(224,240):
	print('multicast')
elif ip == '255.255.255.255':
	print('local broadcast')
elif ip == '0.0.0.0':
	print('unassigned')
else:
	print('unused')
