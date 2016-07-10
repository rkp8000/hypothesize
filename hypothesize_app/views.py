from __future__ import division, print_function, unicode_literals
from datetime import datetime
from unidecode import unidecode

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import generic

import backup
import forms
import models
import node_processing
import search


class Index(generic.TemplateView):

    template_name = 'hypothesize_app/index.html'


class DocumentSearch(generic.ListView):

    template_name = 'hypothesize_app/document_search.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""

        context = super(DocumentSearch, self).get_context_data(**kwargs)

        context['document_search_form'] = forms.DocumentSearchForm(self.request.GET)

        return context

    def get_queryset(self):

        full_list = search.document_query(self.request.GET.get('query', ''))

        return full_list[:int(self.request.GET.get('max_hits', 20))]


class DocumentDetail(generic.DetailView):
    """
    Automatically look for template "document_detail.html".
    To change this, change the template_name class variable.
    """

    model = models.Document

    def get_object(self):

        doc = models.Document.objects.get(pk=self.kwargs['pk'])

        doc.last_viewed = datetime.now()

        doc.save()

        return doc


class DocumentChange(generic.UpdateView):
    """
    Update the contents of a document.
    """

    template_name = 'hypothesize_app/document_form.html'
    form_class = forms.DocumentForm

    def get_object(self):

        doc = models.Document.objects.get(pk=self.kwargs['pk'])

        doc.last_viewed = datetime.now()

        doc.save()

        return doc

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(DocumentChange, self).get_context_data(**kwargs)

        # add in tab complete options

        context['document_pk_list'] = [str(pk) for pk in models.Document.objects.values_list('id', flat=True)]
        context['author_pk_list'] = [str(pk) for pk in models.Author.objects.values_list('id', flat=True)]
        context['publication_name_list'] = [
            str(unidecode(pub))
            for pub in models.Document.objects.values_list('publication', flat=True).distinct()
        ]

        # add in deletion option

        context['include_delete'] = True

        return context


class DocumentCreate(generic.CreateView):
    """
    Add a new document.
    """

    template_name = 'hypothesize_app/document_form.html'
    form_class = forms.DocumentForm

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(DocumentCreate, self).get_context_data(**kwargs)

        # add in tab complete options

        context['document_pk_list'] = [str(pk) for pk in models.Document.objects.values_list('id', flat=True)]
        context['author_pk_list'] = [str(pk) for pk in models.Author.objects.values_list('id', flat=True)]
        context['publication_name_list'] = [
            str(unidecode(pub))
            for pub in models.Document.objects.values_list('publication', flat=True).distinct()
        ]

        return context


class DocumentDelete(generic.DeleteView):
    """
    Delete a document.
    """

    model = models.Document
    success_url = reverse_lazy('hypothesize_app:document_search')


class NodeSearch(generic.ListView):

    template_name = 'hypothesize_app/node_search.html'
    context_object_name = 'nodes'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""

        context = super(NodeSearch, self).get_context_data(**kwargs)

        context['node_search_form'] = forms.NodeSearchForm(self.request.GET)

        return context

    def get_queryset(self):

        full_list = search.node_query(self.request.GET.get('query', ''))

        return full_list[:int(self.request.GET.get('max_hits', 20))]


class NodeDetail(generic.DetailView):
    """
    Automatically look for template "node_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Node

    def get_object(self):

        node = models.Node.objects.get(pk=self.kwargs['pk'])

        node.last_viewed = datetime.now()

        node.save()

        return node


class NodeChange(generic.UpdateView):

    template_name = 'hypothesize_app/node_form.html'
    form_class = forms.NodeForm

    def get_object(self):

        node = models.Node.objects.get(pk=self.kwargs['pk'])

        node.last_viewed = datetime.now()

        node.save()

        return node

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(NodeChange, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = node_processing.make_tab_complete_options(
            document_model=models.Document, node_model=models.Node,
        )

        # add in deletion option

        context['include_delete'] = True

        return context


class NodeCreate(generic.CreateView):

    template_name = 'hypothesize_app/node_form.html'
    form_class = forms.NodeForm

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(NodeCreate, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = node_processing.make_tab_complete_options(
            document_model=models.Document, node_model=models.Node,
        )

        return context


class NodeDelete(generic.DeleteView):

    model = models.Node
    success_url = reverse_lazy('hypothesize_app:node_search')


class NodeTypeSearch(generic.ListView):

    template_name = 'hypothesize_app/node_type_search.html'
    context_object_name = 'node_types'

    def get_queryset(self):

        return models.NodeType.objects.all()


class NodeTypeDetail(generic.DetailView):

    template_name = 'hypothesize_app/node_type_detail.html'
    model = models.NodeType
    context_object_name = 'node_type'


class NodeTypeChange(generic.UpdateView):

    template_name = 'hypothesize_app/node_type_form.html'
    form_class = forms.NodeTypeForm

    def get_object(self):

        return models.NodeType.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(NodeTypeChange, self).get_context_data(**kwargs)

        # add deletion option

        context['include_delete'] = True

        return context


class NodeTypeCreate(generic.CreateView):

    template_name = 'hypothesize_app/node_type_form.html'
    form_class = forms.NodeTypeForm


class NodeTypeDelete(generic.DeleteView):

    template_name = 'hypothesize_app/node_type_confirm_delete.html'
    model = models.NodeType
    success_url = reverse_lazy('hypothesize_app:node_type_search')


class AjaxLinkFetcher(generic.View):

    def get(self, request):

        link_type, link_pk = request.GET['linkpk'].split('-', 1)

        context = {
            'MEDIA_URL': '/media/',
        }

        if link_type == 'document':

            obj = models.Document.objects.get(pk=link_pk)

            context['document'] = obj

            html = render_to_string('hypothesize_app/document_detail_content_only.html', context)

        elif link_type == 'node':

            obj = models.Node.objects.get(pk=link_pk)

            context['node'] = obj

            html = render_to_string('hypothesize_app/node_detail_content_only.html', context)

        anchor = '<a href="{}">(open as new page)</a>'.format(obj.get_absolute_url())

        data = {
            'html': html,
            'anchor': anchor,
        }

        return JsonResponse(data)


class AjaxNodeSaver(generic.View):
    """
    View for saving nodes without reloading page.
    """

    def get(self, request):

        # get node if it exists already, otherwise create it

        try:

            node = models.Node.objects.get(pk=self.request.GET['id'])

            node_save_message = 'Node found.'

        except:

            node = models.Node(id=self.request.GET['id'])

            node_save_message = 'New node created.'

        # TODO: FIGURE OUT PROPER EXCEPTION HANDLING IF PRIMARY KEY UNIQUENESS ERROR

        node.text = self.request.GET['text']

        node.save()

        return JsonResponse({'node_save_message': node_save_message})


class DatabaseBackup(generic.TemplateView):

    template_name = 'hypothesize_app/database_backup.html'

    def get_context_data(self, **kwargs):

        context = super(DatabaseBackup, self).get_context_data(**kwargs)

        if self.request.GET.get('backup', False) == 'TRUE':

            context['backup_result'] = backup.back_up_db()

        return context