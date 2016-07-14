"""
Functions for searching crossref for document metadata.
"""
from difflib import SequenceMatcher
import json

from habanero import Crossref

N_TOP_ITEMS = 5


def get_abstract(item):
    """
    NOT IMPLEMENTED YET

    Attempt to find the item's abstract using a combination of biopython and web scraping.

    :param item: crossref item corresponding to a document
    :return: abstract string if found, otherwise empty string
    """

    return ''


def get_metadata_from_title(title):

    cr = Crossref()

    x = cr.works(query=title)

    top_items = x['message']['items'][:N_TOP_ITEMS]

    # rank top titles in order of string similarity to queried title

    def match(item):

        return SequenceMatcher(None, item['title'][0], title).ratio()

    top_item = sorted(top_items, key=match)[-1]

    # attempt to find abstract

    top_item['abstract'] = get_abstract(top_item)

    return top_item