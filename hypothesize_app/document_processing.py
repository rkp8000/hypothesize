from __future__ import division, print_function, unicode_literals
import re
import string
import urllib

import unidecode

ALPHABET = string.ascii_uppercase


def bind_authors(document, author_model):
    """
    Read a document's author text and bind the appropriate authors.
    :param document: document
    :param author_model: models.Author
    """

    # get author strings from author text

    author_strings = [author_string.strip() for author_string in document.author_text.split(';')]

    document.authors.clear()

    # get/make authors referenced by this article

    for author_string in author_strings:

        if author_string:

            # get or create new author (with pk as unicode author string) and add it to the document

            author = author_model.objects.get_or_create(name=unidecode.unidecode(author_string))[0]

            document.authors.add(author)


def bind_linked_documents(document, document_model):
    """
    Parse a document's linked_documents_text field and bind the relevant documents to it.
    :param document: document
    :param document_model: models.Document
    """

    candidate_keys = [el.strip() for el in document.linked_document_text.split(' ')]

    linked_documents = [document_model.objects.get(key=key) for key in candidate_keys if key]

    document.linked_documents.clear()
    document.linked_documents.add(*linked_documents)


def make_base_key(document):
    """
    Create the base key for a document, which is the last name of the first author
    concatenated with the year.

    :param document: document in question
    :return: base key
    """

    # generate processed version of first author's last name (alphabetic characters only)

    first_author_last_name = document.author_text.split(';')[0].split(',')[0].strip()

    processed_name = first_author_last_name.title().replace(' ', '')

    processed_name = unidecode.unidecode(processed_name)

    processed_name = ''.join([ch for ch in processed_name if ch.isalpha()])

    if not processed_name:

        processed_name = 'Unknown'

    # add year to get base key

    if document.year:

        base_key = '{}{}'.format(processed_name, document.year)

    else:

        base_key = '{}0000'.format(processed_name)

    return base_key


def get_base_key(key):
    """
    Remove duplicate-indicating primary key extensions.

    E.g., convert Smith2001A to Smith2001

    :param key: AuthorYEARC key with potential suffix
    :return: stripped base key
    """

    base_key_pattern = '[a-zA-z]+\d+'

    return re.search(base_key_pattern, key).group(0)


def make_key(document, document_model):
    """
    Generate a unique key for a document.
    The primary key will be the last name of the first author (minus any spaces or fancy characters)
    and the year the article was published, with A, B, ... following that if there already exists a
    document with the given primary key.

    :param document: document
    :param document_model: models.Document
    """

    base_key = make_base_key(document)

    # find all documents that start with this base key

    conflicting_keys = document_model.objects.filter(key__startswith=base_key).values_list('key', flat=True)

    if not conflicting_keys:

        return base_key

    else:

        # TODO: go on to AA, BB, ... if more than 26 conflicting pks exist
        suffix_list = [''] + list(ALPHABET)

        # find the next available key

        for suffix in suffix_list:

            next_key = '{}{}'.format(base_key, suffix)

            if next_key not in conflicting_keys:

                return next_key


def google_scholar_search_url(document):
    """
    Generate the url corresponding to a Google Scholar search for the document's title.
    :param document: document
    """

    prefix = 'https://scholar.google.com/scholar'

    if document.title:

        suffix = urllib.urlencode({'hl': 'en', 'q': document.title.encode('utf-8')})

    else:

        suffix = ''

    return '?'.join([prefix, suffix])
