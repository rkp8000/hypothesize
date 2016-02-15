from __future__ import division, print_function
from datetime import datetime

from django.shortcuts import render, get_object_or_404

import forms
import models
import node_processing

try:
    DEFAULT_DOCUMENTS_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_DOCUMENTS_TO_SHOW').value
    DEFAULT_NODES_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_NODES_TO_SHOW').value
except:
    pass


def index(request):
    return render(request, 'hypothesize_app/index.html')


def document_search(request, n_documents=DEFAULT_DOCUMENTS_TO_SHOW):

    # check if a search query has been sent
    if request.GET:
        # search some stuff
        document_search_form = forms.DocumentSearchForm(request.GET)
        if document_search_form.is_valid():
            documents = document_search_form.get_articles_from_query()
        else:
            documents = models.Document.objects.order_by('-last_viewed')[:n_documents]
    else:
        # make new search form
        document_search_form = forms.DocumentSearchForm()
        # get most recently viewed articles
        documents = models.Document.objects.order_by('-last_viewed')[:n_documents]

    context = {'documents': documents,
               'document_search_form': document_search_form,
               }
    return render(request, 'hypothesize_app/document_search.html', context)


def document_view(request, document_id):
    document = get_object_or_404(models.Document, pk=document_id)
    document.last_viewed = datetime.now()
    document.save()
    context = {
        'file_server_address': None,
        'document': document,
    }

    return render(request, 'hypothesize_app/document_view.html', context)


def document_change(request, document_id):
    pass


def document_add(request):
    pass


def node_search(request, n_nodes=DEFAULT_NODES_TO_SHOW):
    # check if a query has been sent
    if request.GET:
        # search some stuff
        node_search_form = forms.NodeSearchForm(request.GET)
        if node_search_form.is_valid():
            nodes = node_search_form.get_nodes_from_query()
        else:
            nodes = models.Node.objects.order_by('-last_viewed')[:n_nodes]
    else:
        # get most recently viewed nodes
        nodes = models.Node.objects.order_by('-last_viewed')[:n_nodes]
        node_search_form = forms.NodeSearchForm()

    context = {'nodes': nodes,
               'node_search_form': node_search_form}

    return render(request, 'hypothesize_app/node_search.html', context)


def node_view(request, node_id):
    # view a specific node
    node = get_object_or_404(models.Node, pk=node_id)
    # update last viewed field
    node.last_viewed = datetime.now()
    node.save()
    # generate html from node text
    node.html = node_processing.markdown_to_html(node.text)
    context = {'node': node}

    return render(request, 'hypothesize_app/node_view.html', context)


def node_change(request, node_id):
    pass


def node_add(request):
    pass