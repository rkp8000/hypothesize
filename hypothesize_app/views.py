from __future__ import division, print_function
from django.shortcuts import render
import models

DEFAULT_DOCUMENTS_TO_SHOW = models.Setting.objects.get(pk='DEFAULT_DOCUMENTS_TO_SHOW').value

def index(request):
    return render(request, 'hypothesize_app/index.html')

def document_search(request, n_articles=DEFAULT_DOCUMENTS_TO_SHOW):

    context = {'documents': None,
               'document_search_form': None,
               }
    return render(request, 'hypothesize_app/document_search.html', context)

def node_search(request):
    pass