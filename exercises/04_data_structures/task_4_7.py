# -*- coding: utf-8 -*-
'''
Задание 4.7

Преобразовать MAC-адрес mac в двоичную строку такого вида:
'101010101010101010111011101110111100110011001100'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

mac = 'AAAA:BBBB:CCCC'
mac = mac.replace(':', '')

# Solution 1
print(bin(int(mac, 16))[2:])

# Solution 2
print('{:b}'.format(int(mac,16)))

#Все отлично

