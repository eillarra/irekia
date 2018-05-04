irekia
======

[![travis-badge]][travis]
[![coveralls-badge]][coveralls]
[![pypi-badge]][pypi]
[![license-badge]](LICENSE)

This package allows you to communicate with the Open Data Euskadi REST API. Use the `irekia` Client to generate
the convoluted [Open Data Euskadi](http://opendata.euskadi.eus/) query strings and get the data you want.

Installation
------------

Install it using `pipenv`:

```shell
$ pipenv install irekia
```

Usage examples
--------------

Import the Client:

```python
from irekia import Client
```

Results for multiple families, or multiple content_types inside a family
(more information about the available families and content types can be found
[here](http://opendata.euskadi.eus/contenidos-generales/-/familias-y-tipos-de-contenido-de-euskadi-net/):

```python
Client(['eventos', 'opendata']).get()
Client('opendata', ['opendata']).get()
```

Full text search:

```python
Client().search('OpenData').get()
```

Codified queries:

```python
Client('eventos', 'evento').filter(['eventStartDate.GTE.TODAY', 'eventTown.EQ.079']).get()
Client().filter('contentName.EQ.20150929125668').get()
```

Choose language for results:

```python
Client('eventos', 'evento').filter(['eventStartDate.GTE.TODAY', 'eventTown.EQ.079']).get(lang='eu')
```

Changing results' limit (default is 100) and pagination:

```python
Client('eventos', 'evento').limit(20).get(page=5)
```

Ordering of results:

```code-block:: python
Client('opendata').order_by('-documentCreateDate').get()
```

Use the client only to build a URL:

```code-block:: python
Client('eventos', 'evento').order_by('eventStartDate').limit(20).get(page=2, url_only=True)
```

For developers
--------------

To run tests:

```shell
$ pipenv install --dev && pipenv shell
$ tox
```

[travis-badge]: https://api.travis-ci.com/eillarra/irekia.svg
[travis]: https://travis-ci.com/eillarra/irekia
[coveralls-badge]: https://coveralls.io/repos/github/eillarra/irekia/badge.svg
[coveralls]: https://coveralls.io/r/eillarra/irekia
[pypi-badge]: https://badge.fury.io/py/irekia.svg
[pypi]: https://pypi.org/project/irekia/
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
