# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ip = input('Введите IP-адрес: ').strip()

correct_octets_counter = 0

octets = ip.split('.')

if len(octets) == 4:
	for octet in octets:
		if octet.isdigit() and int(octet) in range(0,256):
			correct_octets_counter += 1
		else:
			break

	if correct_octets_counter == 4:
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
	else:
		print('Неправильный IP-адрес')
else:
	print('Неправильный IP-адрес')
