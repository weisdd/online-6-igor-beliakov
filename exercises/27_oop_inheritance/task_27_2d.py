# -*- coding: utf-8 -*-

'''
Задание 27.2d

Дополнить класс MyNetmiko из задания 27.2c или задания 27.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.

Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_27_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_config_set(self, config_commands=None, ignore_errors=True, *args, **kwargs):
        if ignore_errors:
            result = super().send_config_set(config_commands, *args, **kwargs)
        else:
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
    print(r1.send_config_set('lo', ignore_errors=False))


if __name__ == '__main__':
    main()
