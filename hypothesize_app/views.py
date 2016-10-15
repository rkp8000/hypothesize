from __future__ import division, print_function, unicode_literals
from datetime import datetime
import os
from unidecode import unidecode
from urllib import quote

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import generic

import backup
import crossref_search
import document_processing
import forms
import models
import thread_processing
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

    def post(self, request, **kwargs):

        if self.get_form_kwargs()['data']['extract_title_from_pdf']:

            print('Extracting title and binding it to document...')

            try:

                f = request.FILES.get('file', self.get_object().file)

            except:

                f = None

            request.POST['title'] = document_processing.extract_title_from_pdf(f)

        return super(DocumentChange, self).post(request, **kwargs)

    def get_success_url(self):

        success_url = super(DocumentChange, self).get_success_url()

        if self.get_form_kwargs()['data']['extract_title_from_pdf']:

            # swap "detail" for "change"
            # note: this is kind of a hack

            success_url = success_url.rsplit('/detail/', 1)[0] + '/change/'

        return success_url


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

    def post(self, request, **kwargs):

        if self.get_form_kwargs()['data']['extract_title_from_pdf']:

            print('Extracting title and binding it to document...')

            try:

                f = request.FILES['file']

            except:

                f = None

            request.POST['title'] = document_processing.extract_title_from_pdf(f)

        return super(DocumentCreate, self).post(request, **kwargs)

    def get_success_url(self):

        success_url = super(DocumentCreate, self).get_success_url()

        if self.get_form_kwargs()['data']['extract_title_from_pdf']:

            # swap "detail" for "change"
            # note: this is kind of a hack

            success_url = success_url.rsplit('/detail/', 1)[0] + '/change/'

        return success_url


class DocumentDelete(generic.DeleteView):
    """
    Delete a document.
    """

    model = models.Document
    success_url = reverse_lazy('hypothesize_app:document_search')


class ThreadSearch(generic.ListView):

    template_name = 'hypothesize_app/thread_search.html'
    context_object_name = 'threads'

    def get_context_data(self, **kwargs):
        """We'll use this to bulk up later maybe."""

        context = super(ThreadSearch, self).get_context_data(**kwargs)

        context['thread_search_form'] = forms.ThreadSearchForm(self.request.GET)

        return context

    def get_queryset(self):

        full_list = search.thread_query(self.request.GET.get('query', ''))

        return full_list[:int(self.request.GET.get('max_hits', 20))]


class ThreadDetail(generic.DetailView):
    """
    Automatically look for template "thread_detail.html".
    To change this, change the template_name class variable.
    """
    model = models.Thread

    def get_object(self):

        return models.Thread.objects.get(key=self.kwargs['key'])


class ThreadChange(generic.UpdateView):

    template_name = 'hypothesize_app/thread_form.html'
    form_class = forms.ThreadForm

    def get_object(self):

        thread = models.Thread.objects.get(key=self.kwargs['key'])

        # thread.save()

        return thread

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(ThreadChange, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = thread_processing.make_tab_complete_options(
            document_model=models.Document, thread_model=models.Thread)

        # add in deletion option

        context['include_delete'] = True

        return context


class ThreadCreate(generic.CreateView):

    template_name = 'hypothesize_app/thread_form.html'
    form_class = forms.ThreadForm

    def get_context_data(self, **kwargs):

        # get baseline context variables

        context = super(ThreadCreate, self).get_context_data(**kwargs)

        # add in tab complete options

        context['tab_complete_options'] = thread_processing.make_tab_complete_options(
            document_model=models.Document, thread_model=models.Thread)

        # add in deletion option

        context['include_delete'] = True

        return context


class ThreadDelete(generic.DeleteView):

    model = models.Thread
    success_url = reverse_lazy('hypothesize_app:thread_search')


class AjaxLinkFetcher(generic.View):

    def get(self, request):

        link_type, key = request.GET['linkkey'].split('-', 1)

        context = {
            'MEDIA_URL': '/media/',
        }

        try:

            if link_type == 'document':

                obj = models.Document.objects.get(key=key)

                context['document'] = obj
                context['is_internal_link'] = True

                html = render_to_string('hypothesize_app/document_detail_content_only.html', context)

            elif link_type == 'thread':

                obj = models.Thread.objects.get(key=key)

                context['thread'] = obj
                context['is_internal_link'] = True

                html = render_to_string('hypothesize_app/thread_detail_content_only.html', context)

            is_internal_link = True

            data = {
                'html': html,
                'is_internal_link': is_internal_link,
            }

        except Exception as e:

            data = {
                'html': None,
                'is_internal_link': None,
            }

        return JsonResponse(data)


class AjaxDocumentSaver(generic.View):
    """
    View for saving documents without reloading page.
    """

    def post(self, request):

        message = 'AjaxDocumentSaver contacted, data = {}'.format(self.request.POST)

        print(message)

        return JsonResponse({'document_save_message': message})


class AjaxThreadSaver(generic.View):
    """
    View for saving threads without reloading page.
    """

    def post(self, request):

        # validate key

        key_invalid = thread_processing.key_is_invalid(self.request.POST['key'])

        if key_invalid:

            return JsonResponse({'thread_save_message': key_invalid})

        key = self.request.POST['key']

        try:

            quoted_key = quote(key)

        except Exception as e:

            quoted_key = key

        json_response = {'key': key, 'quoted_key': quoted_key}

        # get list of existing keys

        keys_existing = list(models.Thread.objects.values_list('key', flat=True))

        # get the thread if it exists, otherwise attempt to make a new one

        if self.request.POST['id']:

            thread = models.Thread.objects.get(pk=self.request.POST['id'])

            # make sure key is not taken by anything other than fetched thread

            if key in keys_existing and key != thread.key:

                return JsonResponse(
                    {'thread_save_message': '(error: that key is already taken)'}
                )

        else:

            # make sure key is not already taken

            if key in keys_existing:

                return JsonResponse(
                    {'thread_save_message': '(error: that key is already taken)'}
                )

            # make a new thread

            thread = models.Thread(key=key)

            thread.save()

            json_response['new_id'] = thread.id

        # bind key and text to thread

        thread.key = key
        thread.text = self.request.POST['text']

        thread.save()

        thread_save_message = datetime.now().strftime('(thread last saved at %H:%M:%S on %Y-%m-%d)')

        json_response['thread_save_message'] = thread_save_message

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

            return JsonResponse({'error_message': 'an error occurred'})


class DatabaseBackup(generic.TemplateView):

    template_name = 'hypothesize_app/database_backup.html'

    def get_context_data(self, **kwargs):

        context = super(DatabaseBackup, self).get_context_data(**kwargs)

        context['db_backup_dir'] = settings.DATABASE_BACKUP_DIRECTORY
        context['db_dir'] = os.path.dirname(settings.DATABASES['default']['NAME'])

        if self.request.GET.get('backup', False) == 'TRUE':

            context['backup_result'] = backup.back_up_db()

        return context