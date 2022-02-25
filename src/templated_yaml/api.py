import os, yaml
from . import resolver
from .context import Context
from .flatten import flatten_dict


def render_from_path(path, context=None, globals=None):
    """
    Renders a templated yaml document from file path.

    :param path: A path to the yaml file to process.
    :param context: A context to overlay on the yaml file.  This will override any yaml values.
    :param globals: A dictionary of globally-accessible objects within the rendered template.
    :return: A dict with the final overlayed configuration.
    """
    abs_source = os.path.abspath(os.path.expanduser(path))
    yaml_resolver = resolver.TYamlResolver.new_from_path(abs_source)

    return yaml_resolver.resolve(Context(context), globals)._data


def render_from_string(content, context=None, globals=None):
    """
    Renders a templated yaml document from a string.

    :param content: The yaml string to evaluate.
    :param context: A context to overlay on the yaml file.  This will override any yaml values.
    :param globals: A dictionary of globally-accessible objects within the rendered template.
    :return: A dict with the final overlayed configuration.
    """
    yaml_resolver = resolver.TYamlResolver.new_from_string(content)

    return yaml_resolver.resolve(Context(context), globals)._data

def flatten(dictionary):
    """
    Flattens a nested dictionary to key->value pairs.

    :param dictionary: A dictionary of values to flatten.
    """

    return flatten_dict(dictionary)

def to_env(dictionary, prefix=''):
    """
    Convert a key->value pair to env files.

    :param dictionary: A dictionary of values to convert. Nested values are not supported.
    """

    result=''
    prefix=prefix+'_' if prefix else ''
    for key, value in dictionary.items():
        escaped_value=str(value).replace("'", "\\\'")
        result+=f'{prefix.upper()}{key.upper()}=\'{escaped_value}\'\n'

    return result