Connecting to the webserver
###########################

* the webserver is bilbo

.. code-block:: bash

    ssh bilbo.aci.rub.de
    ping www.mofplus.org

* If it was shut down for some reason the docker containers running mofplus and the database have to be restarted

.. code-block:: bash

    docker ps -a # lists all available docker containers
    docker start XXX # starts a container
    docker stop  XXX # stops a container 
    
The important containers are

.. code-block:: bash

    db-weaver
    db-experimental
    db-experimental2
    mofplus

* If you want to access a docker container type

.. code-block:: bash

    docker exec -t -i mofplus bash

* if you afterwards want to get a python console within the MOFplus environment, type

.. code-block:: bash

    python -i web2py.py -vT MOFplus_final2

