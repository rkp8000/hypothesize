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

            documents += list(models.Document.objects.filter(key__iexact=query).all())

        except ObjectDoesNotExist:

            pass

        try:

            documents += list(models.Document.objects.filter(title__iexact=query).all())

        except ObjectDoesNotExist:

            pass

        try:

            documents += list(models.Document.objects.filter(key__contains=query).all())

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

        documents = models.Document.objects.all().order_by('-last_saved')

    return list(unique_everseen(documents))


def thread_query(query):
    """
    Return the threads indexed by a given query.
    :param query: search query (str)
    :return: list of threads
    """

    if query:

        threads = []

        try:

            threads += list(models.Thread.objects.filter(key__iexact=query).all())

        except ObjectDoesNotExist:

            pass

        try:

            threads += list(models.Thread.objects.filter(key__contains=query).all())

        except ObjectDoesNotExist:

            pass

        try:

            threads += list(models.Thread.objects.filter(text__contains=query).all())

        except ObjectDoesNotExist:

            pass

    else:

        threads = models.Thread.objects.all().order_by('-last_saved')

    return list(unique_everseen(threads))