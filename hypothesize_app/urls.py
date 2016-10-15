from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^document/search/$', views.DocumentSearch.as_view(), name='document_search'),
    url(r'^document/(?P<key>.+)/detail/$', views.DocumentDetail.as_view(), name='document_detail'),
    url(r'^document/(?P<key>.+)/change/$', views.DocumentChange.as_view(), name='document_change'),
    url(r'^document/(?P<pk>.+)/delete/$', views.DocumentDelete.as_view(), name='document_delete'),
    url(r'^document/add/$', views.DocumentCreate.as_view(), name='document_create'),

    url(r'^thread/search/$', views.ThreadSearch.as_view(), name='thread_search'),
    url(r'^thread/(?P<key>.+)/detail/$', views.ThreadDetail.as_view(), name='thread_detail'),
    url(r'^thread/(?P<key>.+)/change/$', views.ThreadChange.as_view(), name='thread_change'),
    url(r'^thread/(?P<pk>.+)/delete/$', views.ThreadDelete.as_view(), name='thread_delete'),
    url(r'^thread/new/$', views.ThreadCreate.as_view(), name='thread_create'),

    url(r'^ajax/link_fetcher', views.AjaxLinkFetcher.as_view(), name='ajax_link_fetcher'),
    url(r'^ajax/thread_saver', views.AjaxThreadSaver.as_view(), name='ajax_thread_saver'),
    url(r'^ajax/document_saver', views.AjaxDocumentSaver.as_view(), name='ajax_document_saver'),
    url(r'^ajax/document_autofiller', views.AjaxDocumentAutofiller.as_view(), name='ajax_document_autofiller'),

    url(r'^database_backup/$', views.DatabaseBackup.as_view(), name='database_backup'),
]