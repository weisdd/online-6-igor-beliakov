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

#Все отлично

#вариант решения
ospf_route = "O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"

output = '''
{:25} {}
{:25} {}
{:25} {}
{:25} {}
{:25} {}
{:25} {}
'''

## еще один вариант шаблона
output = '\n{:25} {}'*6

#### Первый вариант: использование срезов
route = ospf_route.split()

print(output.format('Protocol:', 'OSPF',
                    'Prefix:', route[1],
                    'AD/Metric:', route[2][1:-1],
                    'Next-Hop:', route[4][:-1],
                    'Last update:', route[5][:-1],
                    'Outbound Interface:', route[6]))

#### Второй вариант: предварительная обработка строки

# удаляем лишние символы
route = ospf_route.replace(',', ' ').replace('[','').replace(']', '')

# Таким образом можно присвоить несколько переменных за один раз:
_, prefix, ad_metric, _, nhop, update, intf = route.split()

# Тут символ нижнего подчеркивания выполняет специальную роль -
# это те значения, которые нам не нужны и мы хотим их просто выбросить.
# Как вариант, можно было написать и нормальные имена переменных,
# но таким образом, мы явно указываем, что нам не нужны эти значения
# и мы их просто выбрасываем.


print( output.format("Protocol:", "OSPF",
                     "Prefix:", prefix,
                     "AD/Metric:", ad_metric,
                     "Next-Hop:", nhop,
                     "Last update:", update,
                     "Outbound Interface:", intf))
