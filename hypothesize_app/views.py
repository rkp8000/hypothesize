from __future__ import division, print_function, unicode_literals
from datetime import datetime
from unidecode import unidecode

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import generic

import backup
import crossref_search
import forms
import models
import topic_processing
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

        return models.Document.objects.get(key=self.kwargs['key'])


class DocumentChange(generic.UpdateView):
    """
    Update the contents of a document.
    """

    template_name = 'hypothesize_app/document_form.html'
    form_class = forms.DocumentForm

    def get_object(self):

        doc = models.Document.objects.get(key=self.kwargs['key'])

        # TODO: is this save necessary?
        doc.save()

        return doc

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(DocumentChange, self).get_context_data(**kwargs)

        # add in tab complete options

        context['document_key_list'] = [str(key) for key in models.Document.objects.values_list('key', flat=True)]
        context['author_name_list'] = [str(name) for name in models.Author.objects.values_list('name', flat=True)]
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

        context['document_key_list'] = [str(key) for key in models.Document.objects.values_list('key', flat=True)]
        context['author_name_list'] = [str(name) for name in models.Author.objects.values_list('name', flat=True)]
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


class TopicSearch(generic.ListView):

    template_name = 'hypothesize_app/topic_search.html'
    context_object_name = 'topics'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""

        context = super(TopicSearch, self).get_context_data(**kwargs)

        context['topic_search_form'] = forms.TopicSearchForm(self.request.GET)

        return context

    def get_queryset(self):

        full_list = search.topic_query(self.request.GET.get('query', ''))

        return full_list[:int(self.request.GET.get('max_hits', 20))]


class TopicDetail(generic.DetailView):
    """
    Automatically look for template "topic_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Topic

    def get_object(self):

        return models.Topic.objects.get(key=self.kwargs['key'])


class TopicChange(generic.UpdateView):

    template_name = 'hypothesize_app/topic_form.html'
    form_class = forms.TopicForm

    def get_object(self):

        topic = models.Topic.objects.get(key=self.kwargs['key'])

        topic.save()

        return topic

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(TopicChange, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = topic_processing.make_tab_complete_options(
            document_model=models.Document, topic_model=models.Topic)

        # add in deletion option

        context['include_delete'] = True

        return context


class TopicCreate(generic.CreateView):

    template_name = 'hypothesize_app/topic_form.html'
    form_class = forms.TopicForm

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(TopicCreate, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = topic_processing.make_tab_complete_options(
            document_model=models.Document, topic_model=models.Topic)

        # add in deletion option

        context['include_delete'] = True

        return context


class TopicDelete(generic.DeleteView):

    model = models.Topic
    success_url = reverse_lazy('hypothesize_app:topic_search')


class AjaxLinkFetcher(generic.View):

    def get(self, request):

        link_type, key = request.GET['linkkey'].split('-', 1)

        context = {
            'MEDIA_URL': '/media/',
        }

        if link_type == 'document':

            obj = models.Document.objects.get(key=key)

            context['document'] = obj

            html = render_to_string('hypothesize_app/document_detail_content_only.html', context)

        elif link_type == 'topic':

            obj = models.Topic.objects.get(key=key)

            context['topic'] = obj

            html = render_to_string('hypothesize_app/topic_detail_content_only.html', context)

        anchor = '<a href="{}">(open as new page)</a>'.format(obj.get_absolute_url())

        data = {
            'html': html,
            'anchor': anchor,
        }

        return JsonResponse(data)


class AjaxTopicSaver(generic.View):
    """
    View for saving topics without reloading page.
    """

    def get(self, request):

        # make sure topic has key

        key = self.request.GET['key']

        json_response = {'key': key}

        if not key:

            return JsonResponse(
                {'topic_save_message': '(error: you must provide a key)'}
            )

        # make sure key is valid

        invalid_chars = ['"' + char + '"' for char in topic_processing.get_invalid_key_characters(key)]

        if invalid_chars:

            invalid_str = ', '.join(invalid_chars)

            topic_save_message = '(error: the characters {} cannot be used in a key)'.format(invalid_str)

            return JsonResponse(
                {'topic_save_message': topic_save_message})

        # get list of existing keys

        keys_existing = list(models.Topic.objects.values_list('key', flat=True))

        # get the topic if it exists, otherwise attempt to make a new one

        if self.request.GET['id']:

            topic = models.Topic.objects.get(pk=self.request.GET['id'])

            # make sure key is not taken by anything other than fetched topic

            if key in keys_existing and key != topic.key:

                return JsonResponse(
                    {'topic_save_message': '(error: that key is already taken)'}
                )

        else:

            # make sure key is not already taken

            if key in keys_existing:

                return JsonResponse(
                    {'topic_save_message': '(error: that key is already taken)'}
                )

            # make a new topic

            topic = models.Topic(key=key)

            topic.save()

            json_response['new_id'] = topic.id

        # bind key and text to topic

        topic.key = key
        topic.text = self.request.GET['text']

        topic.save()

        topic_save_message = datetime.now().strftime('(topic last saved at %H:%M:%S on %Y-%m-%d)')

        json_response['topic_save_message'] = topic_save_message

        return JsonResponse(json_response)


class AjaxDocumentAutofiller(generic.View):
    """
    View for autofilling document metadata using CrossRef.
    """

    def get(self, request):

        try:

            metadata = crossref_search.get_metadata_from_title_json(self.request.GET['title'])

            return JsonResponse(metadata)

        except:

            return JsonResponse({'error message': 'There was an error fetching.'})


class DatabaseBackup(generic.TemplateView):

    template_name = 'hypothesize_app/database_backup.html'

    def get_context_data(self, **kwargs):

        context = super(DatabaseBackup, self).get_context_data(**kwargs)

        if self.request.GET.get('backup', False) == 'TRUE':

            context['backup_result'] = backup.back_up_db()

        return context