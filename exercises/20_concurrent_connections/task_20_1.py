# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''

from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
import subprocess
import yaml


def ping_ip_addresses(ip_list, limit=3):
    ip_alive = []
    ip_dead = []
    completed_threads = run_threads(ping_ip, ip_list, limit)
    for ip, is_reachable in zip(ip_list, completed_threads):
        ip_alive.append(ip) if is_reachable else ip_dead.append(ip)
    return ip_alive, ip_dead


# Returns True if an ip is reachable and False otherwise
def ping_ip(ip):
    command_output = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                    encoding='utf-8')
    # if returncode == 0 => reachable
    result = True if command_output.returncode == 0 else False
    return result


# Lets run any function as a thread against a list of ips
def run_threads(function, devices, limit):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
        return f_result


def main():
    with open('devices.yaml', 'r', encoding='utf-8') as f:
        devices = yaml.safe_load(f)
        ips = [device['ip'] for device in devices]
        pprint(ping_ip_addresses(ips, 2))


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения
def ping_ip(ip):
    result = subprocess.run(['ping', '-c', '3', '-n', ip],
                            stdout=subprocess.DEVNULL)
    ip_is_reachable = result.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


if __name__ == "__main__":
    print(ping_ip_addresses(['8.8.8.8', '192.168.100.22', '192.168.100.1']))

