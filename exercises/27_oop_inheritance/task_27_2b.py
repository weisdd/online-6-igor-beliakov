# -*- coding: utf-8 -*-

'''
Задание 27.2b

Дополнить класс MyNetmiko из задания 27.2a.

Переписать метод send_config_set netmiko, добавив в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_27_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

'''

import re
from netmiko.cisco.cisco_ios import CiscoIosBase

from task_27_2a import ErrorInCommand


class MyNetmiko(CiscoIosBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()

    def _check_error_in_command(self, command, command_output):
        error_msg_ios = re.search(r'^% (.+)\n', command_output, flags=re.M)
        if error_msg_ios:
            error_msg_raise = (f'При выполнении команды "{command}" на устройстве {self.host}'
                               f' возникла ошибка -> {error_msg_ios.group(1)}')
            raise ErrorInCommand(error_msg_raise)

    def send_command(self, command, *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, command_output)
        return command_output

    def send_config_set(self, config_commands=None, *args, **kwargs):
        if config_commands is None:
            return ""
        elif isinstance(config_commands, str):
            config_commands = (config_commands,)
        result = ''
        for command in config_commands:
            command_output = super().send_config_set(command, *args, **kwargs)
            self._check_error_in_command(command, command_output)
            result += command_output
        return result


device_params = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}


def main():
    r1 = MyNetmiko(**device_params)
    print(r1.send_config_set('lo'))


if __name__ == '__main__':
    main()

# Все отлично

