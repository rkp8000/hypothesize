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

        topic = models.Topic.objects.get(pk=self.kwargs['pk'])

        topic.last_viewed = datetime.now()

        topic.save()

        return topic


class TopicChange(generic.UpdateView):

    template_name = 'hypothesize_app/topic_form.html'
    form_class = forms.TopicForm

    def get_object(self):

        topic = models.Topic.objects.get(pk=self.kwargs['pk'])

        topic.last_viewed = datetime.now()

        topic.save()

        return topic

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(TopicChange, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = topic_processing.make_tab_complete_options(
            document_model=models.Document, topic_model=models.Topic,
        )

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
            document_model=models.Document, topic_model=models.Topic,
        )

        return context


class TopicDelete(generic.DeleteView):

    model = models.Topic
    success_url = reverse_lazy('hypothesize_app:topic_search')


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

        elif link_type == 'topic':

            obj = models.Topic.objects.get(pk=link_pk)

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

        # make sure topic has ID

        if not self.request.GET['id']:

            return JsonResponse(
                {'topic_save_message': '(Error: you must provide an ID.)'}
            )

        # get original topic or try to make a new one

        if self.request.GET['id'] == self.request.GET['initial_id']:

            topic = models.Topic.objects.get(pk=self.request.GET['id'])

        else:

            # attempt to create new topic

            try:

                models.Topic.objects.get(pk=self.request.GET['id'])

                return JsonResponse(
                    {'topic_save_message': '(Error: a topic with that ID already exists.)'})

            except:

                topic = models.Topic(id=self.request.GET['id'])

        topic.text = self.request.GET['text']

        topic.save()

        topic_save_message = datetime.now().strftime('(topic last saved at %H:%M:%S on %Y-%m-%d)')

        json_response = JsonResponse(
            {'topic_save_message': topic_save_message, 'new_id': topic.id})

        return json_response


class DatabaseBackup(generic.TemplateView):

    template_name = 'hypothesize_app/database_backup.html'

    def get_context_data(self, **kwargs):

        context = super(DatabaseBackup, self).get_context_data(**kwargs)

        if self.request.GET.get('backup', False) == 'TRUE':

            context['backup_result'] = backup.back_up_db()

        return context