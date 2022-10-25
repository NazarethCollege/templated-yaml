try:
    from collections import Mapping
except ImportError:
    from collections.abc import Mapping

class ContextInitializationError(Exception):
    pass

class Context(object):

    def __init__(self, data=None, parent=None):
        self._data = data or {}
        self._parent = parent

        if not isinstance(self._data, Mapping):
            raise ContextInitializationError("Root configuration data must be a mapping, structures like lists are not allowed.")

    @property
    def data(self):
        parent = None
        if self.parent:
            parent = self.parent.data

        return {**self._data, **{ 'parent': parent}}

    @property
    def parent(self):
        return self._parent

    def add_parent(self, parent_context):
        if not self.parent:
            self._parent = Context()

        self.parent.overlay(parent_context.data)

    def add(self, additional_context):
        if not isinstance(additional_context, Mapping):
            raise ContextInitializationError("Root configuration data must be a mapping, structures like lists are not allowed.")

        self._data = {**additional_context, **self._data}

    def delete_node(self, key_chain):
        """
        key_chain is an array of keys giving the path to the node that should be deleted.
        """
        node = self._data
        for key in key_chain[:-1]:
            node = node[key]

        del node[key_chain[-1]]

    def overlay(self, additional_context):
        if not isinstance(additional_context, Mapping):
            raise ContextInitializationError("Root configuration data must be a mapping, structures like lists are not allowed.")

        self._data = {**self._data, **additional_context}

    def items(self):
        return self._data.items()

    def __getitem__(self, key):
        if key == 'parent':
            return self.parent

        return self._data[key]