.. molsys documentation master file, created by
   sphinx-quickstart on Mon Aug 21 14:29:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Download and Installation
#########################

Download the code
-----------------

The latest stable source code release can be downloaded here:

.. code-block:: bash

    git clone https://github.com/mofplus_rel


Dependencies
------------

In order to use the MOFplus API the following PYTHON packages has to be installed:

* molsys
* `XMLRPCLIB <https://docs.python.org/2/library/xmlrpclib.html>`_

Further recommended packages are:

* `Sphinx <http://www.sphinx-doc.org>`_ needed if you want to compile the 
  documentation
* `Sphinx rtd theme <https://pypi.python.org/pypi/sphinx_rtd_theme>`_ needed if
  you want to compile the documentation


Installation
------------

In order to install the MOFplus API on your system you have to make sure that the 
mofplus/mofplus directory is in the PYTHONPATH of your system.

If you want to compile the documentation switch to the docs directory and type the follwoing
commands:

.. code-block:: bash
    
    cd docs
    make html

Afterwards you can open the documentation which a browser like firefox.

.. code-block:: bash
    
    firefox _build/html/index.html


