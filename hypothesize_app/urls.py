from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^document/search/$', views.DocumentSearch.as_view(), name='document_search'),
    url(r'^document/(?P<pk>[\w-]+)/detail/$', views.DocumentDetail.as_view(), name='document_detail'),
    url(r'^document/(?P<pk>[\w-]+)/change/$', views.DocumentChange.as_view(), name='document_change'),
    url(r'^document/add/$', views.DocumentCreate.as_view(), name='document_create'),

    url(r'^node/search/$', views.NodeSearch.as_view(), name='node_search'),
    url(r'^node/(?P<pk>[/\w\s-]+)/detail/$', views.NodeDetail.as_view(), name='node_detail'),
    url(r'^node/(?P<pk>[/\w\s-]+)/change/$', views.NodeChange.as_view(), name='node_change'),
    url(r'^node/new/$', views.NodeCreate.as_view(), name='node_create'),
]