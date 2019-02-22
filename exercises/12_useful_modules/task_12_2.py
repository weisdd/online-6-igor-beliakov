# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция check_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''

import ipaddress


def convert_ranges_to_ip_list(ips, print_errors = False):
	result = []
	for ip in ips:
		try: # We assume any ValueError or IndexError here is due to wrong IP format, thus skip the entry
			if '-' in ip:
				if ip.split('-')[-1].isdigit(): # format: 10.1.1.1-10
					ip_start, ip_diff = ip.split('-')
					ip_diff = int(ip_diff) - int(ip_start.split('.')[-1])
					ip_start = ipaddress.ip_address(ip_start)
					ip_stop = ip_start + ip_diff # 10.1.1.10-1 will be also valid
				else: # format: 10.1.1.1-10.1.1.10
					ip_start, ip_stop = [ipaddress.ip_address(i) for i in ip.split('-')]
				if ip_stop < ip_start:
					ip_start, ip_stop = ip_stop, ip_start
				ip_current = ip_start
				while ip_current <= ip_stop:
					result.append(str(ip_current))
					ip_current += 1
			else: # format: 8.8.4.4
				if(ipaddress.ip_address(ip)): # ValueError if it's not an IP address
					result.append(ip)
		except (ValueError, IndexError) as err:
			if print_errors: print(f'{err}. Original argument: "{ip}"')
	return result

def main():
	print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132', '1.2.3',
									 '1.2.3.4-', '1.2.3.5-9'], print_errors = True))


if __name__ == '__main__':
	main()

