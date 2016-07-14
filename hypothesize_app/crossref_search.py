"""
Functions for searching crossref for document metadata.
"""
from difflib import SequenceMatcher

from habanero import Crossref

N_TOP_ITEMS = 5


def get_metadata_from_title(title):

    cr = Crossref()

    x = cr.works(query=title)

    top_items = x['message']['items'][:N_TOP_ITEMS]

    # rank top titles in order of string similarity to queried title

    def match(item):

        return SequenceMatcher(None, item['title'][0], title).ratio()

    top_item = sorted(top_items, key=match)[-1]

    return top_items, top_item