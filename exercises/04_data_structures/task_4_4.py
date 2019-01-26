# -*- coding: utf-8 -*-
'''
Задание 4.4

Список vlans это список VLANов, собранных со всех устройств сети,
поэтому в списке есть повторяющиеся номера VLAN.

Из списка нужно получить уникальный список VLANов,
отсортированный по возрастанию номеров.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

vlans = [10, 20, 30, 1, 2, 100, 10, 30, 3, 4, 10]

# Solution 1
uniq_vlans = list(sorted(set(vlans)))
# Solution 2
uniq_vlans2 = []
for vlan in vlans:
	if vlan not in uniq_vlans2:
		uniq_vlans2.append(vlan)
uniq_vlans2.sort()
print(uniq_vlans)
print(uniq_vlans2)
