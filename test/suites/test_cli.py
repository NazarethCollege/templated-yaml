import os, subprocess, yaml
from test_api import get_test_paths, get_contents, config_path


def run_command(*args, **kwargs):
    stdin_pipe = None
    if kwargs.get('stdin_content'):
        stdin_content = kwargs.pop('stdin_content')
        stdin_pipe, stdin_pipe_write = os.pipe()
        os.write(stdin_pipe_write, stdin_content.encode("utf-8"))
        os.close(stdin_pipe_write)

    tyaml_binary = os.environ['TYAML_EXECUTABLE']
    return subprocess.run([tyaml_binary] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin_pipe, check=True)


def test_render_from_args():
    input, output = get_test_paths('tyaml.variable-substitution')
    processed_cli_output = yaml.safe_load(run_command('render', input).stdout)
    expected_output = yaml.safe_load(get_contents(output))

    assert processed_cli_output == expected_output


def test_render_from_stdin():
    input, output = get_test_paths('tyaml.variable-substitution')


    processed_cli_output = yaml.safe_load(run_command('render', stdin_content=yaml.dump(yaml.safe_load(open(input, 'r')), default_flow_style=False)).stdout)
    expected_output = yaml.safe_load(get_contents(output))

    assert processed_cli_output == expected_output


def test_version():
    version = run_command('version')
    assert version.returncode == 0
    assert os.environ['TYAML_VERSION'] in str(version.stdout)

