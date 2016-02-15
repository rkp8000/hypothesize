from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^document/search/$', views.document_search, name='document_search'),
    url(r'^document/add/$', views.document_add, name='document_add'),
    url(r'^document/(?P<document_id>[\w-]+)/view/$', views.document_view, name='document_view'),
    url(r'^node/search/$', views.node_search, name='node_search'),
]