#!/usr/bin/env python

try:
    from lxml import etree
except Exception as e:
    import sys
    sys.exit('You need to install the `lxml` package to regenerate the metadata file.')

import json
import os
import requests


class MetadataParser(object):
    url = 'http://opendata.euskadi.eus/contenidos-generales/-/familias-y-tipos-de-contenido-de-euskadi-net/'
    metadata = {}

    def parse(self):
        res = requests.get(self.url)
        tree = etree.fromstring(res.text, parser=etree.HTMLParser())
        e_metadata = []

        for c in tree.xpath('(//div[@class="tabbody div_c div_c_euskadi"])[1]/table/tbody/tr'):
            e_metadata.append(c.findall('./td')[0].text)

        e_metadata.sort()
        self.metadata['__euskadi__'] = e_metadata

        for f in tree.xpath('//ul[@id="menu_tipology"]/li'):
            family = f.attrib['id'].split('-')[1]
            f_metadata = []

            xpath = '(//div[@class="tabbody div_f div_f_{0}"])[2]/table/tbody/tr'.format(family)
            for m in tree.xpath(xpath):
                f_metadata.append(m.findall('./td')[0].text)

            f_metadata.sort()
            self.metadata[family] = f_metadata

            for t in f.xpath('.//li'):
                content_type = t.attrib['id'].split('-')[1]
                t_metadata = []

                xpath = '(//div[@class="tabbody div_t div_t_{0}"])[2]/table/tbody/tr'.format(content_type)
                for ct in tree.xpath(xpath):
                    t_metadata.append(ct.findall('./td')[0].text)

                t_metadata.sort()
                self.metadata['{0}.{1}'.format(family, content_type)] = t_metadata

        return self.metadata

    def generate_file(self):
        current_dir = os.path.dirname(__file__)
        metadata_file = os.path.join(current_dir, 'irekia/data/metadata.json')

        with open(metadata_file, 'w') as outfile:
            json.dump(self.parse(), outfile, sort_keys=True, indent=4)

        return self.metadata


MetadataParser().generate_file()
