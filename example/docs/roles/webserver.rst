

``Roles-webserver [init]``
***************************

.. state:: roles.webserver

*Ensure the 'webserver' role has been configured*



Includes
^^^^^^^^

    * :state:`apache`

Steps
^^^^^
1. ``webserver_content_deployed``
    Deploy the webserver content after Apache has been installed

