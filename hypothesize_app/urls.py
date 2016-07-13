from django.conf.urls import url

from hypothesize_app import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^document/search/$', views.DocumentSearch.as_view(), name='document_search'),
    url(r'^document/(?P<key>.+)/detail/$', views.DocumentDetail.as_view(), name='document_detail'),
    url(r'^document/(?P<key>.+)/change/$', views.DocumentChange.as_view(), name='document_change'),
    url(r'^document/(?P<key>.+)/delete/$', views.DocumentDelete.as_view(), name='document_delete'),
    url(r'^document/add/$', views.DocumentCreate.as_view(), name='document_create'),

    url(r'^topic/search/$', views.TopicSearch.as_view(), name='topic_search'),
    url(r'^topic/(?P<key>.+)/detail/$', views.TopicDetail.as_view(), name='topic_detail'),
    url(r'^topic/(?P<key>.+)/change/$', views.TopicChange.as_view(), name='topic_change'),
    url(r'^topic/(?P<key>.+)/delete/$', views.TopicDelete.as_view(), name='topic_delete'),
    url(r'^topic/new/$', views.TopicCreate.as_view(), name='topic_create'),

    url(r'^ajax/link_fetcher', views.AjaxLinkFetcher.as_view(), name='ajax_link_fetcher'),
    url(r'^ajax/topic_saver', views.AjaxTopicSaver.as_view(), name='ajax_topic_saver'),

    url(r'^database_backup/$', views.DatabaseBackup.as_view(), name='database_backup'),
]