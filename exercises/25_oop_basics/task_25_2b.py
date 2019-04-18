# -*- coding: utf-8 -*-

'''
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

'''

import telnetlib
import time
import clitable


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

    def send_config_commands(self, commands):
        if type(commands) == str:
            commands = [commands]
        self._write_line('conf t')
        for command in commands:
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
    # print(test.send_show_command('sh ip int bri', 'templates', True))
    print(test.send_config_commands('logging 1.1.1.1'))
    test.t.close()


if __name__ == '__main__':
    main()
