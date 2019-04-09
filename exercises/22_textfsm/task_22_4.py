# -*- coding: utf-8 -*-
'''
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
'''

from netmiko import ConnectHandler
import clitable
import yaml


def send_and_parse_show_command(device_dict, command, templates_path):
    attributes = {'Command': command, 'Vendor': 'cisco_ios'}
    index_file = 'index'
    # Reference to an index file has to be explicitly defined
    cli_table = clitable.CliTable(index_file, template_dir=templates_path)
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        # We need this line to help clitable to automatically choose a respective template
        command_output = '{}{}\n'.format(ssh.find_prompt(), command)
        command_output += ssh.send_command(command)
        cli_table.ParseCmd(command_output, attributes)
        headers = list(cli_table.header)
        data_rows = [list(row) for row in cli_table]
        result = [dict(zip(headers, row)) for row in data_rows]
        return result


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        devices = yaml.safe_load(f)
        print(send_and_parse_show_command(devices[0], 'sh ip int bri', 'templates'))


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения

import os
from pprint import pprint

def send_and_parse_show_command(device_dict, command, templates_path):
    if 'NET_TEXTFSM' not in os.environ:
        os.environ['NET_TEXTFSM'] = templates_path
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command, use_textfsm=True)
    return output


if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), 'templates')
    with open('devices.yaml') as f:
        devices = yaml.load(f, Loader=yaml.FullLoader)
    for dev in devices:
        result = send_and_parse_show_command(dev, 'sh ip int br',
                                             templates_path=full_pth)
        pprint(result, width=120)

########## Второй вариант без использования use_textfsm в netmiko
from task_22_3 import parse_command_dynamic


def send_and_parse_show_command(device_dict, command, templates_path):
    attributes = {'Command': command, 'Vendor': device_dict['device_type']}
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
        parsed_data = parse_command_dynamic(output, attributes,
                                            templ_path=templates_path)
    return parsed_data


if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), 'templates')
    with open('devices.yaml') as f:
        devices = yaml.load(f, Loader=yaml.FullLoader)
    for dev in devices:
        result = send_and_parse_show_command(dev, 'sh ip int br',
                                             templates_path=full_pth)
        pprint(result, width=120)
