Pre-Processors
==========================================

.. toctree::
   :maxdepth: 2


The module also supports pre-processors that are placed under the ``tyaml`` key inside the document.  These pre-processors
are removed from the output document.

tyaml.mixins
------------

Includes the values from a separate yaml document, preserving the child's configuration when a conflict is encountered.

*input.yml*

.. code-block:: yaml

   tyaml.mixins:
     - base.yml

   full_name: "Sir {{ name }}"

*base.yml*

.. code-block:: yaml

    name: John Smith

*output.yml*

.. code-block:: yaml

   name: John Smith
   full_name: "Sir John Smith"

tyaml.mixins -- parent context
~~~~~~~~~~~~~~

Using the tyaml.mixins preprocessor automatically includes a parent variable in the context.  This can be useful to reference an overridden variable
within the child YAML file.  Following is an example of using the parent.

*input.yml*

.. code-block:: yaml
 
  tyaml.mixins:
    - base.yml

  api_root: http://productiondomain.com
  test_api_path: "{{ parent.api_root }}/users"
  production_api_path: "{{ api_root }}/users"

*base.yml*

.. code-block:: yaml

  api_root: http://testdomain.com

*output.yml*

.. code-block:: yaml

  api_root: http://productiondomain.com
  test_api_path: "http://testdomain.com/users"
  production_api_path: "http://productiondomain.com/users"

When using multiple parents, later mixins will override the variables of earlier mixins.  For example:

*input.yml*

.. code-block:: yaml

  tyaml.mixins:
    - newyork.yml
    - miami.yml

  weather: unknown
  description: "It's going to be a {{ parent.weather }} day!"

*newyork.yml*

.. code-block:: yaml

  weather: snowy

*miami.yml*

.. code-block:: yaml

  weather: sunny

*output.yml*

.. code-block:: yaml

  weather: unknown
  description: "It's going to be a sunny day!"

Alternatively you can specify a namespace for your mixin, which will place all parent context within a varible.
This is useful if you are worried about variable collision.

*input.yml*

.. code-block:: yaml

   tyaml.mixins:
     - namespace: prefix 
       file: base.yml

   value: "{{ prefix.value }} John Doe"

*base.yml*

.. code-block:: yaml

    value: Dr

*output.yml*

.. code-block:: yaml

    prefix:
      value: Dr
    value: Dr John Doe