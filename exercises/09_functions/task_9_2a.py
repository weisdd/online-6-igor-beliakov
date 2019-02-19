# -*- coding: utf-8 -*-
'''
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
    - ключи: имена интерфейсов, вида 'FastEthernet0/1'
    - значения: список команд, который надо выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''


trunk_mode_template = [
    'switchport mode trunk', 'switchport trunk native vlan 999',
    'switchport trunk allowed vlan'
]

trunk_config = {
    'FastEthernet0/1': [10, 20, 30],
    'FastEthernet0/2': [11, 30],
    'FastEthernet0/4': [17]
}

def generate_trunk_config(intf_vlan_mapping, trunk_template):	
	result = {}	
	for port in intf_vlan_mapping:	
		result.setdefault(port, [])	
		#result[port].append(f'interface {port}')	
		for command in trunk_mode_template:	
			if 'allowed vlan' in command:	
				result[port].append(f"{command} {','.join([str(vlan) for vlan in intf_vlan_mapping[port]])}")	
			else:	
				result[port].append(command)	
	return result

