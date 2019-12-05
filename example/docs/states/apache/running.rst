:orphan:

``running``
*******************

.. sls:: apache.running

*Ensure the Apache instance is running*



Steps
^^^^^
1. Remove deprecated conf files
    The list of files comes from pillar ``apache:absent_files``
2. ``apache_config_syntax_checked``
    Check the syntax is OK
3. ``apache_running``
    Apache running



:doc:`[apache (main)] <main>`