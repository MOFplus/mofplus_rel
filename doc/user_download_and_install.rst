.. molsys documentation master file, created by
   sphinx-quickstart on Mon Aug 21 14:29:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Download and Installation
#########################

Download the code
-----------------

The latest stable source code release can be downloaded here:

https://www.mofplus.org

Choose a suitable directory, download and unpack the archive


.. code-block:: bash

    curl -kLO https://www.mofplus.org
    tar -xvzf mofplus.tar.gz
    cd mofplus

As alternatice you can get the most recent version by cloning its git repository:

.. code-block:: bash

    git clone https://github.com/MOFplus


Dependencies
------------

In order to use the MOFplus API the following PYTHON packages has to be installed:

* molsys
* `XMLRPCLIB <https://docs.python.org/2/library/xmlrpclib.html>`_


Installation
------------

In order to install the MOFplus API on your system you have to make sure that the 
mofplus/mofplus directory is in the PYTHONPATH of your system.
