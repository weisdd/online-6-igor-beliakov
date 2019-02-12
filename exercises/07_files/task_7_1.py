# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

template = '''
	Protocol:              OSPF
	Prefix:                {prefix}
	AD/Metric:             {ad_metric}
	Next-Hop:              {next_hop}
	Last update:           {last_update}
	Outbound Interface:    {interface}'''

with open('ospf.txt', 'r') as f:
	for line in f:
		line = line.replace(',', '')
		_, prefix, ad_metric, _, next_hop, last_update, interface = line.split()
		ad_metric = ad_metric.strip('[]')
		print(template.format(prefix=prefix, ad_metric=ad_metric, next_hop=next_hop, last_update=last_update, interface=interface))
