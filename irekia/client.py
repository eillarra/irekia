from __future__ import absolute_import

import json
import os
import requests

from collections import OrderedDict

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode


def _sort_dictionary(dictionary):
    output = OrderedDict()

    for key in sorted(dictionary):
        output[key] = dictionary[key]

    return output


def get_metadata(cluster='euskadi'):
    data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'metadata.json')

    with open(data_file_path, 'r') as data_file:
        metadata = json.loads(data_file.read())

    return metadata if cluster is 'euskadi' else []


class Client:
    endpoint = 'http://www.euskadi.eus/r01hSearchResultWar/r01hPresentationXML.jsp'

    def __init__(self, families=[], content_types=[], **kwargs):
        """Initializes the Open Data Euskadi REST API Client.

        Check http://opendata.euskadi.eus/contenidos-generales/-/familias-y-tipos-de-contenido-de-euskadi-net/
        for the available families and content_types."""
        cluster = kwargs.get('cluster', 'euskadi')
        self.cluster, self.families, self.content_types = self.__check_typology(cluster, families, content_types)
        self.metadata = self.__get_metadata()
        self.search_text = None
        self.codified_query_params = {
            'tC': [self.cluster],
            'tF': self.families,
            'tT': self.content_types,
            'm': [],
            'mA': [],
            'cO': [],
            'p': [],
            'pp': ['r01PageSize.100'],
            'o': []
        }

    def __check_typology(self, cluster, families, content_types):
        """Massages the `family` and `content_type` values and returns the values back."""
        families = [families] if isinstance(families, str) else families
        content_types = [content_types] if isinstance(content_types, str) else content_types

        if len(families) > 1 and content_types:
            raise ValueError('You can\'t call the API for multiple content_types and multiple families. '
                             'Possible combinations are: multiple families and no content_types, or multiple '
                             'content_types for one family.')

        return cluster, families, content_types

    def __check_metadata(self, metadata):
        """Raises an Exception if a metadata is not valid for the selected family + content_type combo."""
        if metadata not in self.metadata:
            raise ValueError('Please use a valid metadata: %s' % ', '.join(self.metadata))
        return

    def __get_metadata(self):
        """Returns a list of valid metadata for the current family + content_type combo.

        It also checks if `family` and `content_type` exist in the metadata collection, and raises an
        exception if not. Checks are only made against the 'euskadi' cluster.
        """
        metadata = get_metadata(self.cluster)
        metadata_output = []

        if metadata:
            metadata_output = metadata['__euskadi__']

            try:
                for family in self.families:
                    metadata_output = metadata_output + metadata[family]
                    for content_type in self.content_types:
                        # This will only work if only one family is present
                        metadata_output = metadata_output + metadata['%s.%s' % (family, content_type)]
            except KeyError:
                raise ValueError('Please use a valid family + content_type combo.')

        metadata_output.sort()
        return metadata_output

    def __get_codified_query(self):
        """Returns a `r01kQry` compatible codified query."""
        blocks = []

        for key, value in _sort_dictionary(self.codified_query_params).items():
            if value:
                blocks.append('{}:{}'.format(key, ','.join(value)))

        return ';'.join(blocks)

    def filter(self, metadata_array, operator='AND'):
        """Builds the filter that will be used when getting the data.

        It needs an array of metadata filters in the format specified by the Open Data Euskadi REST API:
        `metadata.OPERATOR.value`. An optional second value can be passed (AND|OR), to determine if the filter
        should match all metadata conditions (ALL) or only one of them (OR). If the operator is not valid a
        ValueError is raised.

        This method also checks if the metadata is valid, comparing it with the metadata collection
        for every typology (family + content_type combo). If the metadata is not valid a ValueError is raised.

        Usage::

        >>> from irekia import Client
        >>> c = Client('eventos', 'evento').filter(['eventEndDate.EQ.TODAY'])
        <Client>
        """
        if operator not in ['AND', 'OR']:
            raise ValueError('Please use a valid operator: AND | OR')

        op = 'mA' if operator == 'AND' else 'cO'
        self.codified_query_params[op] = [metadata_array] if isinstance(metadata_array, str) else metadata_array

        for metadata_filter in self.codified_query_params[op]:
            self.__check_metadata(metadata_filter.split('.')[0])

        return self

    def get(self, **kwargs):
        """Returns a requests.Response object for the specified query.

        This method should be called after the `filter()` and `order_by()` methods and accepts these **kwargs:
            lang: language of the query, 'es' by default
            page: page number to request, 1 by default
            debug: use True to get a response with extra information for debugging
            url_only: use True to get only a URL

        Usage::

        >>> from irekia import Client
        >>> res = Client('eventos', 'evento').filter(['eventEndDate.GTE.TODAY', 'eventTown.EQ.079']).get(lang='eu')
        <requests.Response [200]>
        """
        language = kwargs.get('lang', 'es')
        self.codified_query_params['m'] = ['documentLanguage.EQ.%s' % language]

        query_params = {'r01kLang': language}

        # Complete query params for search() or filter() queries
        if self.search_text:
            query_params.update(_sort_dictionary({
                'fullText': self.search_text,
                'resultsSource': 'fullText'
            }))
        else:
            query_params.update({'r01kQry': self.__get_codified_query()})

        # Complete query params with pagination, if needed
        page = int(kwargs.get('page', 1))
        if page > 1:
            query_params.update(_sort_dictionary({
                'r01kPgCmd': 'next',
                'r01kSrchSrcId': 'contenidos.inter',
                'r01kTgtPg': page
            }))

        # Set special debug param
        if kwargs.get('debug', False):
            query_params['r01kDebug'] = 'true'

        url = '{}{}{}'.format(self.endpoint, '?', urlencode(_sort_dictionary(query_params)))

        if kwargs.get('url_only', False):
            return url

        return requests.get(url)

    def limit(self, limit=100):
        """Sets the number of results that will be shown per page.

        Usage::

        >>> from irekia import Client
        >>> c = Client('eventos', 'evento').limit(30)
        <Client>
        """
        self.codified_query_params['pp'] = ['r01PageSize.%d' % limit]
        return self

    def order_by(self, *args):
        """Sets an order for the query from metadata *args.

        A `DESC` order can be specified adding a min sign (-) to the metadata name: '-eventStartDate'.

        Usage::

        >>> from irekia import Client
        >>> c = Client('eventos', 'evento').order_by('eventTown', '-eventStartDate')
        <Client>
        """
        for arg in args:
            order = '.'.join([arg[1:], 'DESC']) if arg.startswith('-') else '.'.join([arg, 'ASC'])
            self.__check_metadata(order.split('.')[0])
            self.codified_query_params['o'].append(order)

        return self

    def search(self, search_text):
        """Builds a full text query.

        Usage::

        >>> from irekia import Client
        >>> c = Client().search('OpenData')
        <Client>
        """
        self.search_text = search_text
        return self
