.. _installation:

Installation
============

StorLever is web service designed to ease the management of various
storage resource on your CentOS/RHEL 6 server. It is based on the brilliant 
Python web framework `Pyramid <http://www.pylonsproject.org/>`_.

It requires Python 2.6 or higher, but Python 3k is not supported.

.. _virtualenv:

virtualenv
----------

It is recommended to use virtualenv for Python library management. Though there might
be only one Python interpreter install, virtualenv can make your system looks like having 
multiple Python installations, with each has its own set of libraries independently from others,
therefor there will never be library version conflicts for different projects.

For more about this topic, check out its official document 
`virtualenv <http://www.virtualenv.org/en/latest/>`_

.. _source_code:

Install from Source Code
-----------

You can always find the source code of StorLever on github https://github.com/OpenSight/StorLever,
to check out the latest version::

    $ git clone https://github.com/OpenSight/StorLever.git
    
StorLever is not production-ready, for development purpose, install it as a
development package::
    
    $ python setup.py develop
    
For Development
---------------

For test run or debug, it's better to stick with the development server, which can automatically
reload your code when code change found, and it can printout useful debug information when unexpected
exception raised in the code, and some other helpful functionality for code debug::

    $ pserve --reload storlever_dev.ini

Now you should be able to call REST API via <server_ip>:6543
