# -*- coding: utf-8 -*-
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
'''

import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException


def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            result = ssh.send_command(command)
            return result
    except NetMikoAuthenticationException as err:
        print(err)


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        command = 'sh ip int br'
        devices = yaml.safe_load(f)
        for device in devices:
            print(send_show_command(device, command))


if __name__ == '__main__':
    main()
