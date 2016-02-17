from __future__ import division, print_function
import string

import unidecode

ALPHABET = string.ascii_uppercase


def bind_authors(document, author_model):
    """
    Read a document's author text and bind the appropriate authors.
    :param document:
    :param author_model:
    :return:
    """

    pass


def bind_linked_documents(document, document_model):
    """
    Parse a document's linked_documents_text field and bind the relevant documents to it.
    :param document: document
    :param document_model: models.Document
    """

    candidate_pks = [el.strip() for el in document.linked_document_text.split(' ')]
    print(candidate_pks)
    linked_documents = [document_model.objects.get(pk=pk) for pk in candidate_pks if pk]

    document.linked_documents.clear()
    document.linked_documents.add(*linked_documents)
    print(document.linked_documents)


def bind_primary_key(document, document_model):
    """
    Generate a unique primary key and bind it to the document.
    The primary key will be the last name of the first author (minus any spaces or fancy characters)
    and the year the article was published, with A, B, ... following that if there already exists a
    document with the given primary key.

    :param document: document
    :param document_model: models.Document
    """

    # generate processed version of first author's last name
    first_author_last_name = document.author_text.split(';')[0].split(',')[0].strip()
    processed_name = first_author_last_name.title().replace(' ', '')
    processed_name = unidecode.unidecode(processed_name)
    processed_name = ''.join([ch for ch in processed_name if ch.isalpha()])

    if not processed_name:
        processed_name = 'Unknown'

    # add year to get candidate primary key
    if document.year:
        candidate_pk = '{}{}'.format(processed_name, document.year)
    else:
        candidate_pk = '{}0000'.format(processed_name)

    # find all documents that start with this primary key
    conflicting_pks = document_model.objects.filter(id__startswith=candidate_pk).values_list('id', flat=True)

    if not conflicting_pks:
        pk = candidate_pk
    else:
        # TODO: go on to AA, BB, ... if more than 26 conflicting pks exist
        suffix_list = [''] + list(ALPHABET)

        # find the next available pk
        for suffix in suffix_list:

            candidate_pk_next = '{}{}'.format(candidate_pk, suffix)

            if candidate_pk_next not in conflicting_pks:
                pk = candidate_pk_next
                break

    document.id = pk