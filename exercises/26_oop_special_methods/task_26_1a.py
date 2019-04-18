# -*- coding: utf-8 -*-

'''
Задание 26.1a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 25.1x или задания 26.1.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
'''

topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        filtered_topology = {}
        for local, remote in topology_dict.items():
            if remote not in filtered_topology:
                filtered_topology[local] = remote
        return filtered_topology

    def delete_link(self, local, remote):
        if local in self.topology:
            del (self.topology[local])
        elif remote in self.topology:
            del (self.topology[remote])
        else:
            print('Такого соединения нет')

    def delete_node(self, device):
        initial_size = len(self.topology)
        self.topology = {local: remote for local, remote in self.topology.items() if
                         device not in local and device not in remote}
        if len(self.topology) == initial_size:
            print('Такого устройства нет')

    def add_link(self, local, remote):
        if self.topology.get(local) == remote or self.topology.get(remote) == local:
            print('Такое соединение существует')
        elif local in self.topology or remote in self.topology:
            print('Cоединение с одним из портов существует')
        else:
            self.topology[local] = remote

    def __add__(self, other_topology):
        return Topology({**self.topology, **other_topology.topology})

    def __iter__(self):
        return iter([(local, remote) for local, remote in self.topology.items()])


def main():
    t = Topology(topology_example)
    for link in t:
        print(link)


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения
class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        normalized_topology = {}
        for box, neighbor in topology_dict.items():
            if not neighbor in normalized_topology:
                normalized_topology[box] = neighbor
        return normalized_topology

    def __add__(self, other):
        return Topology({**self.topology, **other.topology})

    def __iter__(self):
        return iter(self.topology.items())
