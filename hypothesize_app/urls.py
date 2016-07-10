from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^document/search/$', views.DocumentSearch.as_view(), name='document_search'),
    url(r'^document/(?P<pk>.+)/detail/$', views.DocumentDetail.as_view(), name='document_detail'),
    url(r'^document/(?P<pk>.+)/change/$', views.DocumentChange.as_view(), name='document_change'),
    url(r'^document/(?P<pk>.+)/delete/$', views.DocumentDelete.as_view(), name='document_delete'),
    url(r'^document/add/$', views.DocumentCreate.as_view(), name='document_create'),

    url(r'^node/search/$', views.NodeSearch.as_view(), name='node_search'),
    url(r'^node/(?P<pk>.+)/detail/$', views.NodeDetail.as_view(), name='node_detail'),
    url(r'^node/(?P<pk>.+)/change/$', views.NodeChange.as_view(), name='node_change'),
    url(r'^node/(?P<pk>.+)/delete/$', views.NodeDelete.as_view(), name='node_delete'),
    url(r'^node/new/$', views.NodeCreate.as_view(), name='node_create'),

    url(r'^node_type/search/$', views.NodeTypeSearch.as_view(), name='node_type_search'),
    url(r'^node_type/(?P<pk>.+)/detail/$', views.NodeTypeDetail.as_view(), name='node_type_detail'),
    url(r'^node_type/(?P<pk>.+)/change/$', views.NodeTypeChange.as_view(), name='node_type_change'),
    url(r'^node_type/(?P<pk>.+)/delete/$', views.NodeTypeDelete.as_view(), name='node_type_delete'),
    url(r'^node_type/new/$', views.NodeTypeCreate.as_view(), name='node_type_create'),

    url(r'^ajax/link_fetcher', views.AjaxLinkFetcher.as_view(), name='ajax_link_fetcher'),
    url(r'^ajax/node_saver', views.AjaxNodeSaver.as_view(), name='ajax_node_saver'),

    url(r'^database_backup/$', views.DatabaseBackup.as_view(), name='database_backup'),
]