# -*- coding: utf-8 -*-
'''
Задание 5.2a

Всё, как в задании 5.2. Но, если пользователь ввел адрес хоста, а не адрес сети,
то надо адрес хоста преобразовать в адрес сети и вывести адрес сети и маску, как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.1/30 - хост из сети 10.0.5.0/30

Если пользователь ввел адрес 10.0.1.1/24,
вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

cidr = input('Введите IP-сеть в формате CIDR (e.g. 10.1.1.0/24): ').strip()
network, bits = cidr.split('/')
bits = int(bits)
octets = [int(octet) for octet in network.split('.')]
# Вычисляем двоичное представление маски сети
full_mask_bin = '1' * bits + '0' * (32-bits)
# Слайсами делим на октеты
mask_octets = [0 for i in range(4)]
mask_octets[0] = int(full_mask_bin[0:8], 2)
mask_octets[1] = int(full_mask_bin[8:16], 2)
mask_octets[2] = int(full_mask_bin[16:24], 2)
mask_octets[3] = int(full_mask_bin[24:32], 2)
# Через binary AND вычисляем адрес сети
octets[0] = octets[0] & mask_octets[0]
octets[1] = octets[1] & mask_octets[1]
octets[2] = octets[2] & mask_octets[2]
octets[3] = octets[3] & mask_octets[3]

template = '''
Network:
{0:<8} {1:<8} {2:<8} {3:<10}
{0:08b} {1:08b} {2:08b} {3:08b}

Mask:
{4:<8} {5:<8} {6:<8} {7:<8}
{4:08b} {5:08b} {6:08b} {7:08b}

'''

print(template.format(octets[0], octets[1], octets[2], octets[3],
	mask_octets[0], mask_octets[1], mask_octets[2], mask_octets[3]))
