import pytest
import task_15_3
import sys
sys.path.append('..')

from common_functions import check_function_exists


def test_function_created():
    check_function_exists(task_15_3, 'convert_ios_nat_to_asa')


def test_function_return_value(asa_nat_config, tmpdir):
    dest_filename = tmpdir.mkdir("test_tasks").join("task_15_3.txt")
    return_value = task_15_3.convert_ios_nat_to_asa('cisco_nat_config.txt',
                                                    dest_filename)
    assert return_value == None, "Функция должна возвращать None"
    assert dest_filename.read().strip() == asa_nat_config.strip(), "Неправильная конфигурация для ASA"

