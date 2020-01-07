:orphan:

``apache.running (state)``
**********************************

.. state:: apache.running

*Ensure the Apache instance is running*

This state makes use of pillar data in :pillar:`apache`

Steps
^^^^^
1. Remove deprecated conf files
    The list of files comes from pillar ``apache:absent_files``
2. ``apache_config_syntax_checked``
    Check the syntax is OK
3. ``apache_running``
    Apache running




`[Source] <https://bitbucket.tools.ficoccs-dev.net/projects/DEVOPS/repos/salt-master-fileset/browse/states/apache/running.sls>`_
:doc:`[apache (main)] <main>`