import pytest


@pytest.fixture(scope='session')
def access_vlans_mapping():
    access_config = {
        'FastEthernet0/12': 10,
        'FastEthernet0/14': 11,
        'FastEthernet0/16': 17
    }
    return access_config


@pytest.fixture(scope='session')
def trunk_vlans_mapping():
    trunk_config = {
        'FastEthernet0/1': [10, 20, 30],
        'FastEthernet0/2': [11, 30],
        'FastEthernet0/4': [17]
    }
    return trunk_config


@pytest.fixture(scope='session')
def template_access_mode():
    access_mode_template = [
        'switchport mode access', 'switchport access vlan',
        'switchport nonegotiate', 'spanning-tree portfast',
        'spanning-tree bpduguard enable'
    ]
    return access_mode_template


@pytest.fixture(scope='session')
def template_psecurity():
    port_security_template = [
        'switchport port-security maximum 2',
        'switchport port-security violation restrict',
        'switchport port-security'
    ]
    return port_security_template


@pytest.fixture(scope='session')
def template_trunk_mode():
    trunk_mode_template = [
        'switchport mode trunk', 'switchport trunk native vlan 999',
        'switchport trunk allowed vlan'
    ]
    return trunk_mode_template

