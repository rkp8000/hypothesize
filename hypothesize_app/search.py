from __future__ import division, print_function, unicode_literals

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
            documents += list(models.Document.objects.filter(id__iexact=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            documents += list(models.Document.objects.filter(title__iexact=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            documents += list(models.Document.objects.filter(id__contains=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            documents += list(models.Document.objects.filter(title__contains=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            documents += list(models.Document.objects.filter(abstract__contains=query).all())
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
    if query:
        nodes = []
        try:
            nodes += list(models.Node.objects.filter(id__iexact=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            nodes += list(models.Node.objects.filter(title__iexact=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            nodes += list(models.Node.objects.filter(id__contains=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            nodes += list(models.Node.objects.filter(title__contains=query).all())
        except ObjectDoesNotExist:
            pass
        try:
            nodes += list(models.Node.objects.filter(text__contains=query).all())
        except ObjectDoesNotExist:
            pass
    else:
        nodes = models.Node.objects.all()
    return list(unique_everseen(nodes))