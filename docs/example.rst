Documentation Example
=======================
In the ``example`` directory of this project is a mock-up of the Salt fileset location (e.g. ``/srv/salt``)
containing ``states``, ``pillar`` and ``reactor`` sub-directories and relevant sls files.

Also located in there is a ``docs`` directory which contains a Sphinx document ``conf.py`` file using the parent
``sphinxcontrib-autosaltsls`` module from the project and the generated .rst files from a build. This allows for
comparing the source sls files with the expected output.

As this is a working configuration, it can be re-run from within the ``example/docs`` directory as follows:

.. code-block:: bash

    sphinx-build -E -b html . _build/html
