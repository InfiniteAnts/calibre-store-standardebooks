# -*- coding: utf-8 -*-


__license__ = 'GPL 3'
__copyright__ = '2020, Anant Ahuja <anant_ahuja@outlook.com>'
__docformat__ = 'restructuredtext en'

from contextlib import closing

from PyQt5.Qt import QUrl

from calibre import (browser, guess_extension)
from calibre.gui2 import open_url
from calibre.utils.xml_parse import safe_xml_fromstring
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog
from .standard_ebooks_description import Description
from calibre.utils.opensearch.query import Query

BASE_URL = 'https://standardebooks.org'


def open_search(url, query, max_results=10, timeout=60):
    description = Description(url)

    url_template = description.get_best_template()

    if not url_template:
        return
    oquery = Query(url_template)

    # set up initial values
    oquery.searchTerms = query
    oquery.count = max_results
    url = oquery.url()

    counter = max_results
    br = browser()
    with closing(br.open(url, timeout=timeout)) as f:
        doc = safe_xml_fromstring(f.read())
        for data in doc.xpath('//*[local-name() = "entry"]'):
            if counter <= 0:
                break

            counter -= 1

            s = SearchResult()

            s.detail_item = ''.join(data.xpath(
                './*[local-name() = "id"]/text()')).strip()

            for link in data.xpath('./*[local-name() = "link"]'):
                rel = link.get('rel')
                href = BASE_URL + link.get('href')
                type = link.get('type')
                title = link.get('title')
                ext = None

                if rel and href and type:
                    if 'http://opds-spec.org/image/thumbnail' == rel:
                        s.cover_url = href
                    elif 'http://opds-spec.org/acquisition/open-access' == rel:
                        if type == 'application/epub+zip' and title == 'Recommended compatible epub':
                            ext = 'EPUB'
                        elif type == 'application/x-mobipocket-ebook':
                            ext = 'AZW3'

                        if ext:
                            s.downloads[ext] = href

            s.formats = ', '.join(s.downloads.keys()).strip()

            s.title = ' '.join(data.xpath(
                './*[local-name() = "title"]//text()')).strip()
            s.author = ', '.join(data.xpath(
                './*[local-name() = "author"]//*[local-name() = "name"]//text()')).strip()

            s.drm = SearchResult.DRM_UNLOCKED
            s.price = '$0.00'

            yield s


class OpenSearchOPDSStore(StorePlugin):

    open_search_url = ''
    web_url = ''

    def open(self, parent=None, detail_item=None, external=False):
        if not hasattr(self, 'web_url'):
            return

        if external or self.config.get('open_external', False):
            open_url(QUrl(detail_item if detail_item else self.web_url))
        else:
            d = WebStoreDialog(self.gui, self.web_url, parent,
                               detail_item, create_browser=self.create_browser)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec_()

    def search(self, query, max_results=10, timeout=60):

        if not getattr(self, 'open_search_url', None):
            return
        for result in open_search(self.open_search_url, query, max_results=max_results, timeout=timeout):
            yield result
