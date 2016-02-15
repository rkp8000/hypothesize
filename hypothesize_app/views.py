from __future__ import division, print_function
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic

import forms
import models
import node_processing

try:
    DEFAULT_DOCUMENTS_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_DOCUMENTS_TO_SHOW').value
    DEFAULT_NODES_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_NODES_TO_SHOW').value
except:
    pass


class IndexView(generic.View):

    def get(self, request):
        return render(request, 'hypothesize_app/index.html')


class DocumentSearchView(generic.ListView):

    template_name = 'hypothesize_app/document_search.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(DocumentSearchView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Document.objects.order_by('-last_viewed')


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


class NodeSearchView(generic.ListView):

    template_name = 'hypothesize_app/node_search.html'
    context_object_name = 'nodes'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(NodeSearchView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Node.objects.order_by('-last_viewed')


def node_view(request, node_id):
    # view a specific node
    node = get_object_or_404(models.Node, pk=node_id)
    # update last viewed field
    node.last_viewed = datetime.now()
    node.save()
    # generate html from node text
    node.html = node_processing.text_to_html(node.text)
    context = {'node': node}

    return render(request, 'hypothesize_app/node_view.html', context)


def node_change(request, node_id):
    pass


def node_add(request):
    pass