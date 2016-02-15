from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^document/search/$', views.document_search, name='document_search'),
    url(r'^document/(?P<document_id>[\w-]+)/view/$', views.document_view, name='document_view'),
    url(r'^document/(?P<document_id>[\w-]+)/change/$', views.document_change, name='document_change'),
    url(r'^document/add/$', views.document_add, name='document_add'),

    url(r'^node/search/$', views.node_search, name='node_search'),
    url(r'^node/(?P<node_id>[/\w\s-]+)/view/$', views.node_view, name='node_view'),
    url(r'^node/(?P<node_id>[/\w\s-]+)/change/$', views.node_change, name='node_change'),
    url(r'^node/add/$', views.node_add, name='node_add'),
]