States
*************

.. note:: This is a custom index supplied from ``_templates/states`` to be used as an example.

These states can be called on a minion using the ``salt-call state.apply`` command.

.. code-block:: bash

    sudo salt-call state.apply <state> test=False

A highstate can be run using the command ``salt-call state.highstate``.

.. code-block:: bash

    sudo salt-call state.highstate [<topfile>] test=False

Top Files
^^^^^^^^^^
.. toctree::
    :maxdepth: 1


    kickstarting.sls <kickstarting>
    top.sls <top>


Other Files
^^^^^^^^^^^^^^^^
.. toctree::
    :maxdepth: 1


    apache  <apache/main>
    kickstart  <kickstart/main>
    nginx  <nginx>
    nrpe  <nrpe>
    template  <template>