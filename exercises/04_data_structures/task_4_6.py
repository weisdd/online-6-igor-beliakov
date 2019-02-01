# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface     FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'

template = '''
	Protocol:              {protocol}
	Prefix:                {prefix}
	AD/Metric:             {ad_metric}
	Next-Hop:              {next_hop}
	Last update:           {last_update}
	Outbound Interface     {outbound_interface}
	'''

ospf_route = ospf_route.replace(',', '')
ospf_route = ospf_route.replace('via ', '')
ospf_route = ospf_route.replace('O', 'OSPF')
#ospf_route = ospf_route.replace('[', '')
#ospf_route = ospf_route.replace(']', '')

protocol, prefix, ad_metric, next_hop, last_update, outbound_interface = ospf_route.split()
ad_metric = ad_metric.strip('[]')
print(template.format(protocol=protocol, prefix=prefix, ad_metric=ad_metric, next_hop=next_hop, last_update=last_update, outbound_interface=outbound_interface))
