irekia
======

|PyPi| |License|

.. |PyPi| image:: https://badge.fury.io/py/irekia.svg
   :target: https://pypi.python.org/pypi/irekia/
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE

This package allows you to communicate with the Open Data Euskadi REST API. Use the `irekia` Client to generate
the convoluted `Open Data Euskadi <http://opendata.euskadi.eus//>`_ query strings and get the data you want.

Installation
------------

Install it using `pip`:

.. code-block:: shell

    $ pip install irekia

Usage examples
--------------

Import the Client:

.. code-block:: python

   from irekia import Client

Results for multiple families, or multiple content_types inside a family
(more information about the available families and content types can be found
`here <http://opendata.euskadi.eus/contenidos-generales/-/familias-y-tipos-de-contenido-de-euskadi-net/>`_):

.. code-block:: python

    Client(['eventos', 'opendata']).get()
    Client('opendata', ['opendata']).get()

Full text search:

.. code-block:: python

    Client().search('OpenData').get()

Codified queries:

.. code-block:: python

    Client('eventos', 'evento').filter(['eventStartDate.GTE.TODAY', 'eventTown.EQ.079']).get()
    Client().filter('contentName.EQ.20150929125668').get()

Choose language for results:

.. code-block:: python

    Client('eventos', 'evento').filter(['eventStartDate.GTE.TODAY', 'eventTown.EQ.079']).get(lang='eu')

Changing results' limit (default is 100) and pagination:

.. code-block:: python

    Client('eventos', 'evento').limit(20).get(page=5)

Ordering of results:

.. code-block:: python

    Client('opendata').order_by('-documentCreateDate').get()

Use the client only to build a URL:

.. code-block:: python

    Client('eventos', 'evento').order_by('eventStartDate').limit(20).get(page=2, url_only=True)

For developers
--------------

To run tests:

.. code-block:: shell

    $ python setup.py test
