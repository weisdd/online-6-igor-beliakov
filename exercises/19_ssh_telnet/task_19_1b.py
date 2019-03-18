# -*- coding: utf-8 -*-
'''
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
'''

import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException


def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            result = ssh.send_command(command)
            return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as err:
        print(err)


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        command = 'sh ip int br'
        devices = yaml.safe_load(f)
        for device in devices:
            print(send_show_command(device, command))


if __name__ == '__main__':
    main()

# Все отлично

