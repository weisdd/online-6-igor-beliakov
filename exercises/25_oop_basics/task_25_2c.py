# -*- coding: utf-8 -*-

'''
Задание 25.2c

Скопировать класс CiscoTelnet из задания 25.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_25_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "i" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "i"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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


def main():
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}

    test = CiscoTelnet(**r1_params)
    # print(test.send_show_command('sh ip int bri', 'templates', True))
    commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors + correct_commands
    # print(test.send_config_commands(commands, strict=False))
    print(test.send_config_commands(commands, strict=True))
    test.t.close()


if __name__ == '__main__':
    main()
