from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^document/search/$', views.DocumentSearch.as_view(), name='document_search'),
    url(r'^document/(?P<pk>[\[\]\(\)\w-]+)/detail/$', views.DocumentDetail.as_view(), name='document_detail'),
    url(r'^document/(?P<pk>[\[\]\(\)\w-]+)/change/$', views.DocumentChange.as_view(), name='document_change'),
    url(r'^document/(?P<pk>[\[\]\(\)\w-]+)/delete/$', views.DocumentDelete.as_view(), name='document_delete'),
    url(r'^document/add/$', views.DocumentCreate.as_view(), name='document_create'),

    url(r'^node/search/$', views.NodeSearch.as_view(), name='node_search'),
    url(r'^node/(?P<pk>[\[\]\(\)/\w\s-]+)/detail/$', views.NodeDetail.as_view(), name='node_detail'),
    url(r'^node/(?P<pk>[\[\]\(\)/\w\s-]+)/change/$', views.NodeChange.as_view(), name='node_change'),
    url(r'^node/(?P<pk>[\[\]\(\)/\w\s-]+)/delete/$', views.NodeDelete.as_view(), name='node_delete'),
    url(r'^node/new/$', views.NodeCreate.as_view(), name='node_create'),

    url(r'^node_type/search/$', views.NodeTypeSearch.as_view(), name='node_type_search'),
    url(r'^node_type/(?P<pk>[\[\]\(\)/\w\s-]+)/detail/$', views.NodeTypeDetail.as_view(), name='node_type_detail'),
    url(r'^node_type/(?P<pk>[\[\]\(\)/\w\s-]+)/change/$', views.NodeTypeChange.as_view(), name='node_type_change'),
    url(r'^node_type/(?P<pk>[\[\]\(\)/\w\s-]+)/delete/$', views.NodeTypeDelete.as_view(), name='node_type_delete'),
    url(r'^node_type/new/$', views.NodeTypeCreate.as_view(), name='node_type_create'),

    url(None, views.AjaxLinkFetcher.as_view(), name='ajax_link_fetcher'),

    url(r'^migrate_old_database/(?P<dbp>[/\w\s-]+)/$', views.migrate_old_database_view, name='migrate_old_database'),
]