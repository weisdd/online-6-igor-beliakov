# -*- coding: utf-8 -*-
'''
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
'''


import tabulate

def print_ip_table(reachable, unreachable):
	to_print = {}
	to_print['Reachable'] = reachable
	to_print['Unreachable'] = unreachable
	print(tabulate.tabulate(to_print, headers='keys'))
	

def main():
	print_ip_table(['10.1.1.1', '10.1.1.2'], ['10.1.1.7', '10.1.1.8', '10.1.1.9'])


if __name__ == '__main__':
	main()

# Все отлично

# вариант решения
def print_ip_table(reach_ip, unreach_ip):
    table = {'Reachable': reach_ip,
             'Unreachable': unreach_ip}
    print(tabulate(table, headers="keys"))

