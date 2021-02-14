# -*- coding: utf-8 ts=4 sw=4 sts=4 et -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from calibre.customize import StoreBase

__license__ = 'GPL 3'
__copyright__ = '2020, Anant Ahuja <anant_ahuja@outlook.com>'
__docformat__ = 'restructuredtext en'


class StandardEbooksStore(StoreBase):
    name = 'Standard Ebooks'
    version = (0, 1, 0)
    description = 'Free and liberated ebooks, carefully produced for the true book lover.'
    author = 'Anant Ahuja'
    actual_plugin = 'calibre_plugins.store_standardebooks.standardebooks:StandardEbooksStore'
    formats = ['EPUB', 'AZW3']
    drm_free_only = True
