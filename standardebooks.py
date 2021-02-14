# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from calibre.gui2.store.search_result import SearchResult
from .standard_ebooks_opensearch_store import OpenSearchOPDSStore
from calibre.gui2.store.basic_config import BasicStoreConfig

store_version = 1  # Needed for dynamic plugin loading

__license__ = 'GPL 3'
__copyright__ = '2020, Anant Ahuja <anant_ahuja@outlook.com>'
__docformat__ = 'restructuredtext en'


class StandardEbooksStore(BasicStoreConfig, OpenSearchOPDSStore):

    open_search_url = 'https://standardebooks.org/ebooks/opensearch'
    web_url = 'https://standardebooks.org/ebooks'

    # https://standardebooks.org/opds

    def search(self, query, max_results=10, timeout=60):
        for s in OpenSearchOPDSStore.search(self, query, max_results, timeout):
            yield s
