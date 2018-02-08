.. MOFplus documentation master file, created by
   sphinx-quickstart on Sat May 20 21:53:23 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MOF+ API Documentation
=========================

`MOF+ <https://www.mofplus.org>`_ is a web ressource for MOFs and related 
framework materials. Besides MOF structures it hosts framework topologies
and parameters for the 
`MOF-FF forcefield. <https://www.mofplus.org/content/show/MOF-FF>`_
It has a PYTHON API based on 
`XMLRPCLIB <https://docs.python.org/2/library/xmlrpclib.html>`_ which can be 
used to communicate with the MOFplus website.

.. toctree::
   :maxdepth: 2
   :caption: User Documentation:

   user_download_and_install
   user_getting_started



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. autoclass:: mofplus.user.user_api
    :show-inheritance:
    :members:

.. autoclass:: mofplus.ff.FF_api
    :show-inheritance:
    :members:

.. autoclass:: mofplus.admin.admin_api
    :show-inheritance:
    :members:
