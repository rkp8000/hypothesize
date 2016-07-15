"""
Functions for searching crossref for document metadata.
"""
from difflib import SequenceMatcher

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
    """
    Fetch the metadata for a document given its title and return a crossref item dict.
    :param title: title of document
    :return: crossref item dictionary
    """
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


def author_text_from_crossref_item(item):
    """
    Get the author text from a crossref item.
    :param item: crossref item
    :return: single string containing all authors with last name first, separated by semicolons
    """

    return 'Author, Fake; Writer, Phony'

def get_metadata_from_title_json(title):
    """
    Return a json object containing the metadata about a document that can be used to fill in a document
    form.

    :param title: title of document
    :return: json object
    """

    item = get_metadata_from_title(title)

    metadata = {}

    metadata['title'] = item.get('title', title)
    metadata['publication'] = item.get('container-title', '')

    try:

        metadata['year'] = item['issued']['date-parts'][0][0]

    except:

        metadata['year'] = None

    metadata['web_link'] = item.get('URL', '')
    metadata['author_text'] = author_text_from_crossref_item(item)
    metadata['crossref'] = '{}'.format(item)

    return metadata