

``webserver``
*********************

.. sls:: roles.webserver

*Ensure the 'webserver' role has been configured*



Includes
^^^^^^^^

    * :sls:`apache`

Steps
^^^^^
1. ``webserver_content_deployed``
    Deploy the webserver content after Apache has been installed



`[Source] <states/roles/webserver/init.sls>`_