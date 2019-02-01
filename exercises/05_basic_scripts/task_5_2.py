# -*- coding: utf-8 -*-
'''
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

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
full_mask_bin = '1' * bits + '0' * (32-bits)
mask_octets = [0 for i in range(4)]
mask_octets[0] = int(full_mask_bin[0:8], 2)
mask_octets[1] = int(full_mask_bin[8:16], 2)
mask_octets[2] = int(full_mask_bin[16:24], 2)
mask_octets[3] = int(full_mask_bin[24:32], 2)

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
