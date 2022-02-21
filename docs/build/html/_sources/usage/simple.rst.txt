Simple
==========================================

.. toctree::
   :maxdepth: 2


The simplest example is referencing a variable somewhere else in the file.  Consider the following example document named example.yaml

.. code-block:: yaml

   name:
     first: John
     last: Smith

   badge: "{{ name.last }}, {{ name.first }}"

Following is the result of running the ``tyaml render example.yaml`` command.

.. code-block:: yaml

   name:
     first: John
     last: Smith

   badge: "Smith, John"