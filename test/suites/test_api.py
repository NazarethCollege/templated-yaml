import templated_yaml.api as tapi, yaml
from templated_yaml.context import ContextInitializationError
import os
from jinja2 import nodes
from jinja2.ext import Extension
import pytest


def get_test_paths(folder):
    return (config_path(folder, 'input.yml'), config_path(folder, 'expected-output.yml'))


def get_contents(file):
    with open(file, 'r') as stream:
        return stream.read()


def config_path(folder, file):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs/{}/{}'.format(folder, file))


def run_test(test_name, globals=None):
    input, output = get_test_paths(test_name)
    processed_input = { k:v for k,v in tapi.render_from_path(input, globals=globals).items() if k != 'parent' }
    expected_output = yaml.safe_load(get_contents(output))

    assert processed_input == expected_output


def test_simple_render():
    run_test('tyaml.variable-substitution')


def test_nested_render():
    run_test('tyaml.nested-variable-substitution')


def test_extends_render():
    run_test('tyaml.extends')


def test_namespacedextends_render():
    run_test('tyaml.namespaced-extends')


def test_extends_multiple_parents_render():
    run_test('tyaml.extends-multiple-parents')


def test_extends_multiple_mixins_render():
    run_test('tyaml.extends-multiple-mixins')


def test_extends_preserve_child_render():
    run_test('tyaml.extends-preserve-child')


def test_newline_render():
    run_test('tyaml.newline-test')


def test_list_variable_substitution():
    run_test('tyaml.list-variable-substitution')


def test_parent_uses_child_var():
    run_test('tyaml.parent_uses_child_var')


def test_sphinx_examples():
    run_test('tyaml.sphinx.simple')
    run_test('tyaml.sphinx.mixins')
    run_test('tyaml.sphinx.mixins')
    run_test('tyaml.sphinx.parent')
    run_test('tyaml.sphinx.multiple_parent')
    run_test('tyaml.sphinx.parent-namespace')


def test_context_overlay():
    result = tapi.render_from_string("name: wrong", context={ 'name': 'right'})

    assert result['name'] == 'right'


def test_globals():
    def global_func():
        return 'globaled'

    result = tapi.render_from_string("global: '{{ global_func() }}'", globals={ 'global_func': global_func })
    assert result['global'] == 'globaled'


def test_list_at_root():
    with pytest.raises(ContextInitializationError):
        run_test('tyaml.list_at_root')

def test_parent_access():
    run_test('tyaml.parent_access')

def test_variable_type():
    run_test('tyaml.variable_type')

def test_variable_chaining():
    run_test('tyaml.variable_chaining')


def test_complex_multiple_parents():
    run_test('tyaml.complex-multi-parent')


def test_variable_chaining_with_globals():
    def get_a():
        return { 'val': 1 }

    run_test('tyaml.variable_chaining_with_globals', globals={ 'get_a': get_a })