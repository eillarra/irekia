from unittest import TestCase

try:
    from urllib import urlencode, quote
except:
    from urllib.parse import urlencode, quote

from irekia import Client, get_metadata


class TestClient(TestCase):

    def test__check_typology__valid(self):
        Client('opendata', 'estadistica')

    def test__check_typology__multiple_families(self):
        with self.assertRaises(ValueError):
            self.assertTrue(Client(['eventos', 'opendata'], 'estadistica'))

    def test__get_metadata__empty(self):
        self.assertEqual(Client('opendata', cluster='www').metadata, [])

    def test__get_metadata__not_valid(self):
        with self.assertRaises(ValueError):
            self.assertTrue(Client('opendata', 'non-existing'))
        with self.assertRaises(ValueError):
            self.assertTrue(Client('non-existing'))

    def test__get_metadata__valid(self):
        metadata = get_metadata()
        self.assertEqual(
            Client('opendata', 'estadistica').metadata,
            sorted(metadata['__euskadi__'] + metadata['opendata'] + metadata['opendata.estadistica'])
        )

    def test_filter(self):
        with self.assertRaises(ValueError):  # invalid metadata
            self.assertTrue(Client('opendata').filter(['eventEndDate.EQ.TODAY']))
        with self.assertRaises(ValueError):  # invalid operator
            self.assertTrue(Client('eventos', 'evento').filter(['eventEndDate.EQ.TODAY'], operator='MIX'))

        url_and = Client('eventos', 'evento').filter(['eventEndDate.GTE.TODAY', 'eventTown.EQ.079']).get(url_only=True)
        self.assertTrue(quote('mA:eventEndDate.GTE.TODAY,eventTown.EQ.079') in url_and)
        url_or = Client('eventos', 'evento').filter(['eventEndDate.EQ.TODAY'], operator='OR').get(url_only=True)
        self.assertTrue(quote('cO:eventEndDate.EQ.TODAY') in url_or)

    def test_limit(self):
        url = Client('opendata', 'estadistica').limit(30).get(url_only=True)
        self.assertTrue(quote('pp:r01PageSize.30') in url)

    def test_order_by(self):
        url = Client('eventos', 'evento').order_by('eventTown', '-eventStartDate').get(url_only=True)
        self.assertTrue(quote('o:eventTown.ASC,eventStartDate.DESC') in url)

    def test_pagination(self):
        page = 2
        url = Client('eventos', 'evento').get(page=page, url_only=True)
        self.assertTrue(urlencode({'r01kPgCmd': 'next'}) in url)
        self.assertTrue(urlencode({'r01kSrchSrcId': 'contenidos.inter'}) in url)
        self.assertTrue(urlencode({'r01kTgtPg': page}) in url)

    def test_search(self):
        search_text = 'OpenData Euskadi'
        url = Client().search(search_text).get(url_only=True)
        self.assertTrue(urlencode({'fullText': search_text}), url)
        self.assertTrue(urlencode({'resultsSource': 'fullText'}) in url)
