import pytest


@pytest.fixture(scope='session')
def sh_version_r1():
    with open('sh_version_r1.txt') as f:
        return f.read()


@pytest.fixture(scope='session')
def sh_version_r2():
    with open('sh_version_r2.txt') as f:
        return f.read()


@pytest.fixture(scope='session')
def routers_inventory():
    csv_content = [['hostname', 'ios', 'image', 'uptime'],
                   ['r1',
                      '12.4(15)T1',
                      'flash:c1841-advipservicesk9-mz.124-15.T1.bin',
                      '15 days, 8 hours, 32 minutes'],
                   ['r2',
                      '12.4(4)T',
                      'disk0:c7200-js-mz.124-4.T',
                      '45 days, 8 hours, 22 minutes'],
                   ['r3',
                      '12.4(4)T',
                      'disk0:c7200-js-mz.124-4.T',
                      '5 days, 18 hours, 2 minutes']]
    return csv_content


@pytest.fixture(scope='session')
def sh_cdp_n_sw1():
    with open('sh_cdp_n_sw1.txt') as f:
        return f.read()


@pytest.fixture(scope='session')
def list_of_cdp_files():
    sh_cdp_files = ['sh_cdp_n_r2.txt', 'sh_cdp_n_r5.txt',
                    'sh_cdp_n_r1.txt', 'sh_cdp_n_sw1.txt',
                    'sh_cdp_n_r3.txt', 'sh_cdp_n_r4.txt', 'sh_cdp_n_r6.txt']
    return sh_cdp_files


@pytest.fixture(scope='session')
def sh_cdp_topology_dicts():
    correct_cdp_topology = {'R2': {'Eth 0/0': {'SW1': 'Eth 0/2'},
                                   'Eth 0/1': {'R5': 'Eth 0/0'},
                                   'Eth 0/2': {'R6': 'Eth 0/1'}},
                            'R5': {'Eth 0/0': {'R2': 'Eth 0/1'},
                                   'Eth 0/1': {'R4': 'Eth 0/1'}},
                            'R1': {'Eth 0/0': {'SW1': 'Eth 0/1'}},
                            'SW1': {'Eth 0/1': {'R1': 'Eth 0/0'},
                                    'Eth 0/2': {'R2': 'Eth 0/0'},
                                    'Eth 0/3': {'R3': 'Eth 0/0'},
                                    'Eth 0/4': {'R4': 'Eth 0/0'}},
                            'R3': {'Eth 0/0': {'SW1': 'Eth 0/3'}},
                            'R4': {'Eth 0/0': {'SW1': 'Eth 0/4'},
                                   'Eth 0/1': {'R5': 'Eth 0/1'}},
                            'R6': {'Eth 0/1': {'R2': 'Eth 0/2'}}}
    return correct_cdp_topology


@pytest.fixture(scope='session')
def sh_cdp_topology_tuples():
    correct_cdp_topology = {('R1', 'Eth 0/0'): ('SW1', 'Eth 0/1'),
                            ('R2', 'Eth 0/0'): ('SW1', 'Eth 0/2'),
                            ('R2', 'Eth 0/1'): ('R5', 'Eth 0/0'),
                            ('R2', 'Eth 0/2'): ('R6', 'Eth 0/1'),
                            ('R3', 'Eth 0/0'): ('SW1', 'Eth 0/3'),
                            ('R4', 'Eth 0/0'): ('SW1', 'Eth 0/4'),
                            ('R4', 'Eth 0/1'): ('R5', 'Eth 0/1')}
    return correct_cdp_topology
