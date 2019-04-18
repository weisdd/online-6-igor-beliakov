# -*- coding: utf-8 -*-

'''
Задание 25.2

Создать класс CiscoTelnet, который подключается по Telnet к оборудованию Cisco.

При создании экземпляра класса, должно создаваться подключение Telnet, а также переход в режим enable.
Класс должен использовать модуль telnetlib для подключения по Telnet.

У класса CiscoTelnet, кроме __init__, должно быть, как минимум, два метода:
* _write_line - принимает как аргумент строку и отправляет на оборудование строку преобразованную в байты и добавляет перевод строки в конце
* send_show_command - принимает как аргумент команду show и возвращает вывод полученный с обрудования

Пример создания экземпляра класса:
In [2]: from task_25_2 import CiscoTelnet

In [3]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}
   ...:

In [4]: r1 = CiscoTelnet(**r1_params)

In [5]: r1.send_show_command('sh ip int br')
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

'''

import telnetlib
import time


class CiscoTelnet:
    def __init__(self, **kwargs):
        self.t = telnetlib.Telnet(kwargs['ip'])
        self.t.read_until(b'Username:')
        self._write_line(kwargs['username'])
        self.t.read_until(b'Password:')
        self._write_line(kwargs['password'])
        self._write_line('enable')
        self._write_line(kwargs['secret'])
        self._write_line('terminal length 0')
        # Just to clear buffer
        self.t.read_until(b'terminal length 0')
        self.t.read_until(b'#')

    def _write_line(self, command):
        self.t.write(command.encode('utf-8') + b'\n')

    def send_show_command(self, command):
        self._write_line(command)
        time.sleep(3)
        return self.t.read_very_eager().decode('utf-8')


def main():
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}

    test = CiscoTelnet(**r1_params)
    print(test.send_show_command('sh ip int bri'))
    test.t.close()


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения
import time
import telnetlib
import yaml


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username:')
        self._write_line(username)
        self.telnet.read_until(b'Password:')
        self._write_line(password)
        self._write_line('enable')
        self.telnet.read_until(b'Password:')
        self._write_line(secret)
        self._write_line('terminal length 0')
        time.sleep(1)
        self.telnet.read_very_eager()

    def _write_line(self, line):
        self.telnet.write(line.encode('ascii') + b'\n')

    def send_show_command(self, command):
        self._write_line(command)
        time.sleep(1)
        command_output = self.telnet.read_very_eager().decode('ascii')
        return command_output


if __name__ == '__main__':
    r1 = CiscoTelnet(**r1_params)
    print(r1.send_show_command('sh ip int br'))

