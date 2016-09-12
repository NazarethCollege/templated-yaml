import yaml, collections, os
from jinja2 import Template


class TYamlProcessors(object):

    @classmethod
    def mixins(cls, resolver, current_context, value):
        for mixin in value:
            base_file_path = os.path.abspath(os.path.join(
                os.path.dirname(resolver._original_file),
                mixin
            ))

            parent_resolver = TYamlResolver.new_from_path(base_file_path)

            current_context = { **parent_resolver.resolve(current_context), **current_context }

        return current_context

class TYamlResolver(object):

    processors = {
        'tyaml.mixins': TYamlProcessors.mixins
    }

    def __init__(self, data):
        self._original_file = None
        self._data = data

    @classmethod
    def new_from_path(cls, abs_path):
        yaml_source = None

        with open(abs_path, 'r') as stream:
            yaml_source = yaml.load(stream)

        resolver = TYamlResolver(yaml_source)
        resolver._original_file = abs_path

        return resolver

    @classmethod
    def new_from_string(cls, content):
        resolver = TYamlResolver(yaml.load(content))
        resolver._original_file = os.getcwd() + '_in_memory_stream_.yml'

        return resolver

    def resolve(self, context=None):
        if not context: context = {}

        current_context = { **self._data, **context }

        def walk_dict(node, keys=None):
            if not keys: keys = []

            for key, item in node.items():
                key_chain = keys + [key,]

                if isinstance(item, collections.Mapping):
                    for i in walk_dict(item, key_chain): yield i
                else:
                    yield node, key_chain, item

        pre_processors = []

        # get a list of pre-processors to handle tyaml directives easier
        for parent, key_chain, item in walk_dict(current_context):
            key = '.'.join(key_chain)
            processor = TYamlResolver.processors.get(key, None)
            if processor:
                pre_processors += [(processor, item, parent, key_chain[-1])]

        for processor, item, node_parent, node_key in pre_processors:
            del node_parent[node_key]
            current_context = processor(self, current_context, item)

        # do variable substitution on any strings, since they may contain template variables
        for parent, key_chain, item in walk_dict(current_context):
            if isinstance(item, str):
                template = Template(item)
                parent[key_chain[-1]] = template.render(current_context)


        return current_context