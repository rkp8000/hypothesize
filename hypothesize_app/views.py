from __future__ import division, print_function

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views import generic

import forms
import models
import node_processing

try:
    DEFAULT_DOCUMENTS_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_DOCUMENTS_TO_SHOW').value
    DEFAULT_NODES_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_NODES_TO_SHOW').value
except:
    pass


class Index(generic.View):

    def get(self, request):
        return render(request, 'hypothesize_app/index.html')


class DocumentSearch(generic.ListView):

    template_name = 'hypothesize_app/document_search.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(DocumentSearch, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Document.objects.order_by('-last_viewed')


class DocumentDetail(generic.DetailView):
    """
    Automatically look for template "document_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Document


class DocumentChange(generic.UpdateView):
    """
    Update the contents of a document.
    """
    template_name = 'hypothesize_app/document_change.html'
    form_class = forms.DocumentForm

    def get_object(self):
        return models.Document.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # get baseline context variables
        context = super(DocumentChange, self).get_context_data(**kwargs)
        # add in tab complete options
        context['document_pk_list'] = [str(pk) for pk in models.Document.objects.values_list('id', flat=True)]
        return context


class DocumentCreate(generic.CreateView):
    """
    Add a new document.
    """
    template_name = 'hypothesize_app/document_change.html'
    form_class = forms.DocumentForm


class NodeSearch(generic.ListView):

    template_name = 'hypothesize_app/node_search.html'
    context_object_name = 'nodes'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""
        context = super(NodeSearch, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.Node.objects.order_by('-last_viewed')


class NodeDetail(generic.DetailView):
    """
    Automatically look for template "node_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Node


class NodeChange(generic.UpdateView):

    template_name = 'hypothesize_app/node_change.html'
    form_class = forms.NodeForm

    def get_object(self):
        return models.Node.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # get baseline context variables
        context = super(NodeChange, self).get_context_data(**kwargs)
        # add in tab complete options
        context['tab_complete_options'] = node_processing.make_tab_complete_options(
            document_model=models.Document, node_model=models.Node,
        )
        return context


class NodeCreate(generic.CreateView):

    template_name = 'hypothesize_app/node_change.html'
    form_class = forms.NodeForm