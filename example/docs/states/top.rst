``top.sls (state)``
**********************

*Default top file to run on state.highstate*



Environment: base
=======================

Common to all salt environments


``'*'`` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All minions run these states

    * :state:`nrpe`

``'role:webserver'`` (Match: grain)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    * :state:`roles.webserver`

Environment: production
=============================

Production states only


``'role:proxy'`` (Match: grain)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    * :state:`roles.proxy`

`[Source] <https://bitbucket.tools.ficoccs-dev.net/projects/DEVOPS/repos/salt-master-fileset/browse/states/./top.sls>`_