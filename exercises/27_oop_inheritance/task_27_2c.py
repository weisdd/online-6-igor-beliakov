# -*- coding: utf-8 -*-

'''
Задание 27.2c

Проверить, что метод send_command класса MyNetmiko из задания 27.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_27_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

'''

from task_27_2b import MyNetmiko

device_params = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}


def main():
    r1 = MyNetmiko(**device_params)
    print(r1.send_command('sh ip int br', strip_command=False))
    print(r1.send_command('sh ip int br', strip_command=True))


if __name__ == '__main__':
    main()

# Все отлично

