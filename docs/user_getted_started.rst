.. molsys documentation master file, created by
   sphinx-quickstart on Mon Aug 21 14:29:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Getting Started
###############

Setting up your Credentials
---------------------------

For using the MOFplus API it is required to have an user account at www.mofplus.org.
There are two possbilities to tell the API your credentials.

The first possibility is to setup in your home directory a hidden file called ``.mofplusrc``.
In this one you have to give your email adress, which you used to register at MOFplus and
your password. An example is given below::

    lucky.luke@lonesome.de
    rantanplan

If you do not provide such a file, the API is asking you at every startup for your
email adress and password. 

.. warning::

   Credentials are saved as clear text python attributes of the API class
   during a session. Make sure that you use your MOFplus password only for MOFplus.

.. note::
   
   Developers which have a MOFplus application running on localhost can connect with
   the API by setting the environment variable 'MFPDB' to 'LOCAL'.

Programm Structure
------------------

The MOFplus API package is divided modules 

   #. module ``user`` with class ``user_api``. 
         Here all methods for querying
         topology and MOF structure related data are implemented.
   #. module ``ff`` with class ``ff_api``. 
         Here all methods for getting and
         setting force field parameters and reference data are available.
         The ``ff_api`` class is inherited from the ``user_api`` class. So all
         methods implemented in ``user_api`` are also available in ``ff_api``.
   

Using the API
-------------

For a detailed description of all implemented methods please have a look at the
technical documentation section where all three classes are explained in more
detail. How to create instance of the three above described classes is shown
in the following examples:

.. code-block:: python

    >> import mofplus
    >> api = mofplus.user_api()

.. code-block:: python

    >> import mofplus
    >> api = mofplus.FF_api()

The api object can then be used for example to download a topology
stored at MOFplus. 

.. code-block:: python

    >> api.get_net("tbo")
