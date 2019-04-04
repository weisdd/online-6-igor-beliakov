# -*- coding: utf-8 -*-
'''
Задание 21.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 21.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
'''

import re
from netmiko import ConnectHandler
from task_21_1 import generate_config

data = {
    'tun_num': None,
    'wan_ip_1': '192.168.100.1',
    'wan_ip_2': '192.168.100.2',
    'tun_ip_1': '10.0.1.1 255.255.255.252',
    'tun_ip_2': '10.0.1.2 255.255.255.252'
}

src_device_params = {'device_type': 'cisco_ios',
                     'ip': '192.168.100.1',
                     'username': 'cisco',
                     'password': 'cisco',
                     'secret': 'cisco'
                     }

dst_device_params = {'device_type': 'cisco_ios',
                     'ip': '192.168.100.2',
                     'username': 'cisco',
                     'password': 'cisco',
                     'secret': 'cisco'
                     }


def send_command(device, show=None, config=None):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        if show:
            result = ssh.send_command(show)
        elif config:
            result = ssh.send_config_set(config)
        else:
            result = None
    return result


def find_free_tunnel_id(tunnels1, tunnels2):
    # Берём вывод show ip int brief с двух устройств, отыскиваем в нём номера сконфигурированных тоннелей,
    # затем возвращаем первый неиспользованный на обоих устройствах номер (в str - для удобства).
    tunnels = '{}\n{}'.format(tunnels1, tunnels2)
    regex = r'^Tunnel(\d+)\s+'
    taken_tunnel_ids = [int(match.group(1)) for match in re.finditer(regex, tunnels, flags=re.M)]
    if not taken_tunnel_ids:
        return '0'  # default value
    for tunnel_id in range(max(taken_tunnel_ids) + 2):  # upper limit = max + 1
        if tunnel_id not in taken_tunnel_ids:
            return str(tunnel_id)
    # В теории, не должно быть ситуации, когда из find_free_tunnel_id вернётся None (разве что когда range задан
    # неверно. Мб стоит добавить raise, чтобы на устройство потом не отправлялся частичный конфиг.


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    tunnels1 = send_command(src_device_params, show='sh ip int bri | i Tun')
    tunnels2 = send_command(dst_device_params, show='sh ip int bri | i Tun')
    vpn_data_dict['tun_num'] = find_free_tunnel_id(tunnels1, tunnels2)
    result1 = send_command(src_device_params, config=generate_config(src_template, vpn_data_dict))
    result2 = send_command(dst_device_params, config=generate_config(dst_template, vpn_data_dict))
    return f'{result1}\n{result2}'


def main():
    print(configure_vpn(src_device_params,
                        dst_device_params,
                        'templates/gre_ipsec_vpn_1.txt',
                        'templates/gre_ipsec_vpn_2.txt',
                        data))


if __name__ == '__main__':
    main()

# Все отлично

