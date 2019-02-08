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

#Все отлично

#вариант решения
while True:
    ip_address = input('Введите адрес: ')
    ip_list = ip_address.split('.')

    correct_octets = [int(octet) for octet in ip_list
                      if octet.isdigit() and 0 <= int(octet) <= 255]
    ip_correct = len(ip_list) == 4 and len(correct_octets) == 4
    if ip_correct:
        break
    print('Incorrect IPv4 address')

first_octet = correct_octets[0]

if 1 <= first_octet <= 223 :
    print('unicast')
elif 224 <= first_octet <= 239 :
    print('multicast')
elif ip_address == '0.0.0.0':
    print('unassigend')
elif ip_address == '255.255.255.255':
    print ('local broadcast')
else:
    print('unused')
