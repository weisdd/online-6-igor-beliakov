# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''

import yaml
from netmiko import ConnectHandler


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        result = ssh.send_command(command)
        return result


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        command = 'sh ip int br'
        devices = yaml.safe_load(f)
        for device in devices:
            print(send_show_command(device, command))


if __name__ == '__main__':
    main()

# Все отлично
# можно еще добавить переход в enable, так как не все команды выполняются без него

