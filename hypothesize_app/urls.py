from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^document/search/$', views.DocumentSearchView.as_view(), name='document_search'),
    url(r'^document/(?P<pk>[\w-]+)/detail/$', views.DocumentDetailView.as_view(), name='document_detail'),
    url(r'^document/(?P<pk>[\w-]+)/change/$', views.document_change, name='document_change'),
    url(r'^document/add/$', views.document_add, name='document_add'),

    url(r'^node/search/$', views.NodeSearchView.as_view(), name='node_search'),
    url(r'^node/(?P<pk>[/\w\s-]+)/detail/$', views.NodeDetailView.as_view(), name='node_detail'),
    url(r'^node/(?P<pk>[/\w\s-]+)/change/$', views.NodeChangeView.as_view(), name='node_change'),
    url(r'^node/new/$', views.NodeCreateView.as_view(), name='node_create'),
]