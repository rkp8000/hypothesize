"""
Functions for searching crossref for document metadata.
"""
from difflib import SequenceMatcher

from Bio import Entrez
from habanero import Crossref

N_TOP_ITEMS = 5


def get_abstract(item):
    """
    NOT IMPLEMENTED YET

    Attempt to find the item's abstract using a combination of biopython and web scraping.

    :param item: crossref item corresponding to a document
    :return: abstract string if found, otherwise empty string
    """

    fail_message = 'Abstract could not be retrieved.'

    try:

        # give Entrez an email (replace this with your email)

        Entrez.email = "abc@abc.com"

        # search pubmed for title and get top id

        handle = Entrez.esearch(db='pubmed', term=item['title'])
        top_id = Entrez.read(handle)['IdList'][0]

        # fetch metadata for the top pubmed id

        fetch_handle = Entrez.efetch(db='pubmed', id=top_id, retmode='xml')
        data = Entrez.read(fetch_handle)

        return data[0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0]

    except:

        return fail_message


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

    try:

        author_strings = [', '.join([a['family'], a['given']]) for a in item['author']]

        return '; '.join(author_strings)

    except:

        return ''


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

    metadata['abstract'] = item.get('abstract', '')
    metadata['web_link'] = item.get('URL', '')
    metadata['author_text'] = author_text_from_crossref_item(item)
    metadata['crossref'] = '{}'.format(item)

    return metadata