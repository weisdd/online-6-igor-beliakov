# -*- coding: utf-8 -*-
'''
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''

import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler

commands = {'192.168.100.1': 'sh ip int br',
            '192.168.100.2': 'sh arp',
            '192.168.100.3': 'sh ip int br'}


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    all_results = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_ssh = [executor.submit(send_command, device, commands_dict[device['ip']])
                      for device in devices]
        for future in as_completed(future_ssh):
            all_results.append(future.result())
    with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_results))


def send_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = '{}{}\n'.format(ssh.find_prompt(), command)
        result += ssh.send_command(command)
        return result


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        devices = yaml.safe_load(f)
        send_command_to_devices(devices, commands, 'test_20_3.txt', 2)


if __name__ == '__main__':
    main()
