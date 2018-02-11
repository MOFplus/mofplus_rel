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

The first possibility is to setup in your home directory a hidden file called .mofplusrc.
In this one you have to give your email adress, which you used to register at MOFplus and
your password. An example is given below::

    lucky.luke@shootout.de
    lonesome

If you do not provide such a file, the API is asking you at every startup for your
email adress and password. 

.. warning::

   Credentials are safed as clear text python attributes of the API class
   during a session. Make sure that you use your MOFplus password only for MOFplus.

.. note::
   
   Developers which have a MOFplus application running on localhost can connect with
   the API by setting the environment variable 'MFPDB' to 'LOCAL'.

Using the API
-------------

The MOFplus API package is divided into three subclasses called:

   #. user_api
   #. ff_api
   #. admin_api

