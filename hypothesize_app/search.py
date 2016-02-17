from __future__ import division, print_function

import models


def document_query(query):
    """
    Return the documents indexed by a given query.
    :param query: search query (str)
    :return: QuerySet of documents
    """
    return models.Document.objects.all()


def node_query(query):
    """
    Return the nodes indexed by a given query.
    :param query: search query (str)
    :return: QuerySet of nodes
    """
    return models.Node.objects.all()