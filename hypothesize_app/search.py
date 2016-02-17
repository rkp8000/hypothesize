from __future__ import division, print_function

from django.core.exceptions import ObjectDoesNotExist
from more_itertools import unique_everseen

import models


def document_query(query):
    """
    Return the documents indexed by a given query.
    :param query: search query (str)
    :return: list of documents
    """
    if query:
        documents = []
        try:
            documents.append(models.Document.objects.get(id__iexact=query))
        except ObjectDoesNotExist:
            pass
        try:
            documents.append(models.Document.objects.get(title__iexact=query))
        except ObjectDoesNotExist:
            pass
        try:
            documents.append(models.Document.objects.get(id__contains=query))
        except ObjectDoesNotExist:
            pass
        try:
            documents.append(models.Document.objects.get(title__contains=query))
        except ObjectDoesNotExist:
            pass
        try:
            documents.append(models.Document.objects.get(abstract__contains=query))
        except ObjectDoesNotExist:
            pass
    else:
        documents = models.Document.objects.all()

    return list(unique_everseen(documents))


def node_query(query):
    """
    Return the nodes indexed by a given query.
    :param query: search query (str)
    :return: list of nodes
    """
    return models.Node.objects.all()