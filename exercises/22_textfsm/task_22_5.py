# -*- coding: utf-8 -*-
'''
Задание 22.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 22.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
'''

from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from task_22_4 import send_and_parse_show_command
from pprint import pprint
import yaml


def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    '''
    :param devices: список словарей с параметрами подключения к устройствам
    :param command: команда, которую необходимо выполнить на удалённом устройстве
    :param templates_path: путь к файлам с шаблонами TextFSM
    :param limit: количество потоков (по умолчанию, 3).
    :return: список списков с результатами выполнения команды.
    При этом, информация о том, какое именно устройство опрашивалось, не добавляется в вывод.
    '''
    with ThreadPoolExecutor(max_workers=limit) as executor:
        completed_threads = executor.map(send_and_parse_show_command, devices, repeat(command), repeat(templates_path))
        return [result for result in completed_threads]


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        devices = yaml.safe_load(f)
        # В данном случае мы можем использовать вывод, чтобы определить IP-адреса, назначенные на всех интерфейсах,
        # в т.ч. отключенных - иногда это полезно :)
        # Для чего-то более сложного нужно уже интегрировать модуль логгирования.
        pprint(send_and_parse_command_parallel(devices, "sh ip int bri", 'templates', 2))


if __name__ == '__main__':
    main()

# Все отлично

