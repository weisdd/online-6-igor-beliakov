# -*- coding: utf-8 -*-
'''
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

correct_octets_counter = 0
octets = []

while correct_octets_counter != 4:
	correct_octets_counter = 0
	ip = input('Введите IP-адрес: ').strip()
	octets = ip.split('.')
	if len(octets) != 4:
		print('Неправильный IP-адрес')
		break
	for octet in octets:
		if octet.isdigit() and int(octet) in range(0,256):
			correct_octets_counter += 1
		else:
			print('Неправильный IP-адрес')
			break

	first_byte = int(octets[0])
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
