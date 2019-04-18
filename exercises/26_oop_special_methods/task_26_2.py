# -*- coding: utf-8 -*-

'''
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
'''

import telnetlib
import time
import clitable
import re


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

    def _parse_command_dynamic(self, command_output, attributes_dict, index_file='index', templ_path='templates'):
        cli_table = clitable.CliTable(index_file, templ_path)
        cli_table.ParseCmd(command_output, attributes_dict)
        headers = list(cli_table.header)
        result = [dict(zip(headers, list(row))) for row in cli_table]
        return result

    def send_show_command(self, command, templates, parse):
        self._write_line(command)
        time.sleep(3)
        command_output = self.t.read_very_eager().decode('utf-8')
        if parse:
            attributes = {'Command': command, 'Vendor': 'cisco_ios'}
            result = self._parse_command_dynamic(command_output, attributes, templ_path=templates)
        else:
            result = command_output
        return result

    def send_config_commands(self, commands, strict=False):
        result = ''
        if type(commands) == str:
            commands = [commands]
        self._write_line('conf t')
        for command in commands:
            self._write_line(command)
            time.sleep(3)
            command_output = self.t.read_very_eager().decode('utf-8')
            error = re.search(r'^% (.+)\n', command_output, flags=re.M)
            if error:
                error_msg = (f'При выполнении команды "{command}" на устройстве {self.t.host}'
                             f' возникла ошибка -> {error.group(1)}')
                if strict:
                    raise ValueError(error_msg)
                print(error_msg)
            result += command_output
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # It's caller's responsibility to raise exceptions, so here we're just closing the connection
        self.t.close()


def main():
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}

    with CiscoTelnet(**r1_params) as t:
        # print(test.send_show_command('sh ip int bri', 'templates', True))
        commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
        correct_commands = ['logging buffered 20010', 'ip http server']
        commands = commands_with_errors + correct_commands
        # print(test.send_config_commands(commands, strict=False))
        print(t.send_config_commands(commands, strict=True))


if __name__ == '__main__':
    main()

# Все отлично

