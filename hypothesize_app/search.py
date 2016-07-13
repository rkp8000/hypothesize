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

        documents = models.Document.objects.all().order_by('-last_viewed')

    return list(unique_everseen(documents))


def topic_query(query):
    """
    Return the topics indexed by a given query.
    :param query: search query (str)
    :return: list of topics
    """

    if query:

        topics = []

        try:

            topics += list(models.Topic.objects.filter(key__iexact=query).all())

        except ObjectDoesNotExist:

            pass

        try:

            topics += list(models.Topic.objects.filter(key__contains=query).all())

        except ObjectDoesNotExist:

            pass

        try:

            topics += list(models.Topic.objects.filter(text__contains=query).all())

        except ObjectDoesNotExist:

            pass

    else:

        topics = models.Topic.objects.all().order_by('-last_viewed')

    return list(unique_everseen(topics))