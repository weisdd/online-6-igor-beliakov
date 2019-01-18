import pytest
import task_9_4a
import sys
sys.path.append('..')

from common_functions import check_function_exists, check_function_params


def test_function_created():
    check_function_exists(task_9_4a, 'convert_config_to_dict')


def test_function_params():
    check_function_params(function=task_9_4a.convert_config_to_dict,
                          param_count=1, param_names=['config_filename'])


def test_function_return_value():
    control_values = {'hostname PE_r1': [],
                      'interface Ethernet0/1': ['no ip address'],
                      'interface Ethernet0/2': ['description To P_r9 Ethernet0/2',
                                                'ip address 10.0.19.1 255.255.255.0',
                                                'mpls traffic-eng tunnels',
                                                'ip rsvp bandwidth'],
                      'interface Ethernet0/3': ['description To sw1 Ethernet0/3', 'no ip address'],
                      'interface Ethernet0/3.100': {'encapsulation dot1Q 100': [],
                                                    'xconnect 10.2.2.2 12100 encapsulation mpls': ['backup peer 10.4.4.4 14100',
                                                                                                   'backup delay 1 1']},
                      'interface Tunnel0': ['ip unnumbered Loopback0',
                                            'tunnel mode mpls traffic-eng',
                                            'tunnel destination 10.2.2.2',
                                            'tunnel mpls traffic-eng priority 7 7',
                                            'tunnel mpls traffic-eng bandwidth 5000',
                                            'tunnel mpls traffic-eng path-option 10 dynamic',
                                            'no routing dynamic'],
                      'ip access-list standard LDP': ['deny   10.0.0.0 0.0.255.255',
                                                      'permit 10.0.0.0 0.255.255.255'],
                      'router bgp 100': {'address-family vpnv4': ['neighbor 10.2.2.2 activate',
                                                                  'neighbor 10.2.2.2 send-community both',
                                                                  'exit-address-family'],
                                         'bgp bestpath igp-metric ignore': [],
                                         'bgp log-neighbor-changes': [],
                                         'neighbor 10.2.2.2 next-hop-self': [],
                                         'neighbor 10.2.2.2 remote-as 100': [],
                                         'neighbor 10.2.2.2 update-source Loopback0': [],
                                         'neighbor 10.4.4.4 remote-as 40': []},
                      'router ospf 1': ['mpls ldp autoconfig area 0',
                                        'mpls traffic-eng router-id Loopback0',
                                        'mpls traffic-eng area 0',
                                        'network 10.0.0.0 0.255.255.255 area 0']}


    return_value = task_9_4a.convert_config_to_dict('config_r1.txt')
    assert return_value != None, "Функция ничего не возвращает"
    assert type(return_value) == dict, "Функция должна возвращать словарь"
    for key, value in control_values.items():
        assert key in return_value and value == return_value[key], f"Секция {key} не прошла проверку. Смотри словарь control_values в тесте"

