from __future__ import division, print_function
from datetime import datetime

from django.shortcuts import render, get_object_or_404

from forms import DocumentSearchForm
import models

DEFAULT_DOCUMENTS_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_DOCUMENTS_TO_SHOW').value


def index(request):
    return render(request, 'hypothesize_app/index.html')


def document_search(request, n_documents=DEFAULT_DOCUMENTS_TO_SHOW):

    # check if a search query has been sent
    if request.GET:
        # search some stuff
        document_search_form = DocumentSearchForm(request.GET)
        if document_search_form.is_valid():
            documents = document_search_form.get_articles_from_query()
        else:
            documents = models.Document.objects.order_by('-last_viewed')[:n_documents]
    else:
        # make new search form
        document_search_form = DocumentSearchForm()
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

    return render(request, 'hypothesize_app/document_view.html', {'document': document})


def document_change(request, document_id):
    pass

def document_add(request):
    pass


def node_search(request):
    pass