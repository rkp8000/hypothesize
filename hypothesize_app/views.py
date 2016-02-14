from django.shortcuts import render


def index(request):
    return render(request, 'hypothesize_app/index.html')

def document_search(request):
    pass

def node_search(request):
    pass