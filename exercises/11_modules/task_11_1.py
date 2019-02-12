# -*- coding: utf-8 -*-
'''
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент вывод команды одной строкой (не имя файла).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}

В словаре интерфейсы должны быть записаны без пробела между типом и именем. То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


def parse_cdp_neighbors(command_output):
	cdp = command_output.strip().split('\n')
	l_hostname = cdp[0].split('>')[0] # '#' в качестве возможного разделителя не учитываем. 
	cdp_data_flag = 0 # Начались строки с данными о соседях
	result = {}
	for line in cdp:
		if line.startswith('Device ID'):
			cdp_data_flag = 1
			continue
		# Пропускаем все строки до таблицы с нужными нам данные + пустые строки
		if not cdp_data_flag or line.strip() == '': continue
		neighbor = line.split()
		n_hostname = neighbor[0]
		l_intf = neighbor[1] + neighbor[2]
		n_intf = neighbor[-2] + neighbor[-1]
		result[(l_hostname, l_intf)] = (n_hostname, n_intf)
	return result

#Все отлично

#вариант решения
def parse_cdp_neighbors(command_output):
    result = {}
    for line in command_output.split('\n'):
        if '>' in line:
            hostname = line.split('>')[0]
        #отобрать нужные строки можно по последнему столбцу
        # последний символ число - номер интерфейса
        elif line.strip() and line.strip()[-1].isdigit():
            r_host, l_int, l_int_num, *other, r_int, r_int_num = line.split()
            #В other собираются все остальные элементы,
            # которые явно не присваиваются
            result[(hostname, l_int+l_int_num)] = (r_host, r_int+r_int_num)
    return result

if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt', 'r') as show_in:
        print(parse_cdp_neighbors(show_in.read()))
