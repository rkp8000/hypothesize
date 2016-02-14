from django.conf.urls import patterns, url

from hypothesize_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^document/search/$', views.document_search, name='document_search'),
    url(r'^node/search/$', views.node_search, name='node_search'),
)