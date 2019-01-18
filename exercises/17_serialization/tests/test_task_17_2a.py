import os
import yaml
import pytest
import task_17_2a
import sys
sys.path.append('..')

from common_functions import check_function_exists, check_function_params, get_func_params_default_value


def test_function_created():
    check_function_exists(task_17_2a, 'generate_topology_from_cdp')


def test_function_params():
    check_function_params(function=task_17_2a.generate_topology_from_cdp,
                          param_count=2,
                          param_names=['list_of_files', 'save_to_filename'])
    default_values = get_func_params_default_value(task_17_2a.generate_topology_from_cdp)
    assert default_values.get('save_to_filename') == None, "У параметра save_to_filename значение по умолчанию должно быть None"


def test_function_return_value(list_of_cdp_files, sh_cdp_topology_dicts):
    correct_return_value = sh_cdp_topology_dicts

    return_value = task_17_2a.generate_topology_from_cdp(list_of_cdp_files)
    assert return_value != None, "Функция ничего не возвращает"
    assert type(return_value) == dict, "Функция должна возвращать словарь"
    assert return_value == correct_return_value, "Функция возвращает неправильное значение"


def test_writing_to_yaml_file(list_of_cdp_files, sh_cdp_topology_dicts, tmpdir):
    dest_filename = tmpdir.mkdir("test_tasks").join("topology.yaml")
    return_value = task_17_2a.generate_topology_from_cdp(list_of_cdp_files,
                                                         save_to_filename=dest_filename)
    assert os.path.exists(dest_filename), "YAML файл не создан"
    with open(dest_filename) as f:
        yaml_file_content = yaml.load(f)
    assert yaml_file_content == sh_cdp_topology_dicts, "Топология не записана в YAML файл"

