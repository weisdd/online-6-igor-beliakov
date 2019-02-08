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

#Все отлично

#вариант решения
ip_address = input('Enter ip address: ')
octets = ip_address.split('.')
correct_ip = True

if len(octets) != 4:
    correct_ip = False
else:
    for octet in octets:
        if not (octet.isdigit() and int(octet) in range(256)):
            correct_ip = False
            break

if not correct_ip:
    print('Incorrect IPv4 address')
else:
    octets_num = [int(i) for i in octets]

    if octets_num[0] in range(1,224):
        print('unicast')
    elif octets_num[0] in range(224,240):
        print('multicast')
    elif set(octets_num) == {255}:
        print('broadcast')
    elif set(octets_num) == {0}:
        print('unassigned')
    else:
        print('unused')


################################################
# Вариант с проверкой list comprehensions
ip_address = input('Введите IP-адрес в десятично-точечном формате: ')
ip_bytes = ip_address.split('.')

correct = [b for b in ip_bytes if b.isdigit() and 0 <= int(b) <= 255]

if len(correct) != 4 or len(ip_bytes) != 4:
    print('Неправильный IP-адрес')
else:
    ip = [int(i) for i in ip_bytes]

    if ip == [0, 0, 0, 0]:
        print('unassigned')
    elif ip == [255, 255, 255, 255]:
        print('local broadcast')
    elif 1 <= ip[0] <= 223:
        print('unicast')
    elif 224 <= ip[0] <= 239:
        print('multicast')
    else:
        print('unused')
