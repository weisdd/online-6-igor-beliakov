# -*- coding: utf-8 -*-
'''
Задание 19.2a

Скопировать функцию send_config_commands из задания 19.2 и добавить параметр verbose,
который контролирует будет ли выводится на стандартный поток вывода
информация о том к какому устройству выполняется подключение.

По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, verbose=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства из файла devices.yaml с помощью функции send_config_commands.
'''

import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


def send_config_commands(device, config_commands, verbose=True):
    if verbose:
        print(f"Подключаюсь к {device['ip']}...")
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_config_set(config_commands)
            return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as err:
        print(err)


def main():
    commands = [
        'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
    ]
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        devices = yaml.safe_load(f)
        for device in devices:
            print(send_config_commands(device, commands))


if __name__ == '__main__':
    main()
