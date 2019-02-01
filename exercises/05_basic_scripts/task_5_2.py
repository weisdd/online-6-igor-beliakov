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

#Все отлично

#вариант решения
### Вариант без использования генераторов списка

network = input('Введите адрес сети: ')

ip, mask = network.split('/')
ip_list = ip.split('.')
mask = int(mask)

# Преобразуем каждый октет адреса в int
# и записываем каждый октет адреса в отдельную переменную
oct1, oct2, oct3, oct4 = [int(ip_list[0]), int(ip_list[1]),
                          int(ip_list[2]), int(ip_list[3])]

bin_mask = '1' * mask + '0' * (32 - mask)
# Разделение по октетам:
bin_mask = [bin_mask[0:8], bin_mask[8:16], bin_mask[16:24], bin_mask[24:32]]
# Преобразование в int:
m1, m2, m3, m4 = [int(bin_mask[0], 2), int(bin_mask[1], 2),
                  int(bin_mask[2], 2), int(bin_mask[3], 2)]


ip_output = '''
Network:
{0:<8}  {1:<8}  {2:<8}  {3:<8}
{0:08b}  {1:08b}  {2:08b}  {3:08b}'''

mask_output = '''
Mask:
/{0}
{1:<8}  {2:<8}  {3:<8}  {4:<8}
{1:08b}  {2:08b}  {3:08b}  {4:08b}
'''

print(ip_output.format(oct1, oct2, oct3, oct4))
print(mask_output.format(mask, m1, m2, m3, m4))



### Вариант с генераторами списка
ip, mask = network.split('/')
mask = int(mask)

# каждый октет адреса в отдельной переменной
oct1, oct2, oct3, oct4 = [int(i) for i in ip.split('.')]

bin_mask = '1' * mask + '0' * (32 - mask)
# Каждый октет маски в отдельной переменной
m1, m2, m3, m4 = [int(bin_mask[i:i+8], 2) for i in [0, 8, 16, 24]]


ip_output = '''
Network:
{0:<8}  {1:<8}  {2:<8}  {3:<8}
{0:08b}  {1:08b}  {2:08b}  {3:08b}'''

mask_output = '''
Mask:
/{0}
{1:<8}  {2:<8}  {3:<8}  {4:<8}
{1:08b}  {2:08b}  {3:08b}  {4:08b}
'''

print(ip_output.format(oct1, oct2, oct3, oct4))
print(mask_output.format(mask, m1, m2, m3, m4))
