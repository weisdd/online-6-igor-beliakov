# -*- coding: utf-8 -*-
'''
Задание 4.5
Из строк command1 и command2 получить список VLANов,
которые есть и в команде command1 и в команде command2.
Результатом должен быть список: ['1', '3', '8']
Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

command1 = 'switchport trunk allowed vlan 1,2,3,5,8'
command2 = 'switchport trunk allowed vlan 1,3,8,9'

# Solution 1
vlans1 = set(command1.replace('switchport trunk allowed vlan ', '', 1).split(','))
vlans2 = set(command2.replace('switchport trunk allowed vlan ', '', 1).split(','))
result1 = sorted(vlans1.intersection(vlans2))
print(result1)

# Solution 2
vlans3 = command1.replace('switchport trunk allowed vlan ', '', 1).split(',')
vlans4 = command2.replace('switchport trunk allowed vlan ', '', 1).split(',')
result2 = []

for vlan in vlans3:
	if vlan in vlans4:
		result2.append(vlan)
print(result2)

