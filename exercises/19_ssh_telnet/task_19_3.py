# -*- coding: utf-8 -*-
'''
Задание 19.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\nR1(config)#end\nR1#'
'''

import yaml
from task_19_1b import send_show_command
from task_19_2a import send_config_commands


def send_commands(device, show=None, config=None):
    if show:
        result = send_show_command(device, show)
    elif config:
        result = send_config_commands(device, config)
    else:
        result = None
    return result


def main():
    commands = [
        'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
    ]
    command = 'sh ip int br'
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
        for device in devices:
            print(send_commands(device, show=command))
            print(send_commands(device, config=commands))


if __name__ == '__main__':
    main()

# Все отлично
