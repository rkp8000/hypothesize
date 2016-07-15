from __future__ import print_function, unicode_literals
import json
import os

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

import document_processing
import topic_processing


class Author(models.Model):
    """Author class."""

    name = models.CharField(max_length=255, db_index=True, default='')

    def __unicode__(self):

        return self.name


class Document(models.Model):
    """Article class."""

    key = models.CharField(max_length=255, unique=True, default='')
    title = models.CharField(max_length=255, default='')
    author_text = models.TextField(blank=True, default='')
    publication = models.CharField(max_length=100, blank=True, default='')
    year = models.SmallIntegerField(null=True, blank=True)
    abstract = models.TextField(blank=True, default='')
    web_link = models.CharField(max_length=500, blank=True, default='')
    file = models.FileField(upload_to='documents', null=True, blank=True)
    crossref = models.TextField(blank=True, default='')
    uploaded = models.DateTimeField(default=timezone.now, blank=True)
    last_saved = models.DateTimeField(default=timezone.now, blank=True)
    linked_document_text = models.TextField(blank=True, default='')
    linked_documents = models.ManyToManyField('self', symmetrical=False, blank=True)
    authors = models.ManyToManyField(Author, blank=True)

    def __unicode__(self):

        return self.key

    @property
    def primary_external_link(self):

        if self.web_link:

            return self.web_link

        else:

            return document_processing.google_scholar_search_url(self)

    def get_absolute_url(self):

        return reverse('hypothesize_app:document_detail', kwargs={'key': self.key})

    def save(self, *args, **kwargs):
        """
        Override basic save method to extract linked documents.
        """

        # generate key if there wasn't one before

        if not self.key:

            self.key = document_processing.make_key(self, document_model=Document)

        else:

            # change document key if base key has changed

            base_key = document_processing.get_base_key(self.key)

            if base_key != document_processing.make_base_key(self):

                self.key = document_processing.make_key(self, document_model=Document)

        # save the document so we can bind other things to it

        super(Document, self).save(*args, **kwargs)

        document_processing.bind_authors(self, author_model=Author)

        document_processing.bind_linked_documents(self, document_model=Document)

        # update last saved time

        self.last_saved = timezone.now()

        super(Document, self).save(*args, **kwargs)


class Topic(models.Model):
    """Topic class."""

    key = models.CharField(max_length=255, unique=True, default='')
    text = models.TextField(blank=True, default='')
    created = models.DateTimeField(default=timezone.now, blank=True)
    last_saved = models.DateTimeField(default=timezone.now, blank=True)
    topics = models.ManyToManyField('self', symmetrical=False, blank=True)
    documents = models.ManyToManyField(Document, blank=True)

    def save(self, *args, **kwargs):
        """
        Override default method to do additional topic processing.
        """

        # save the topic so we can bind other things to it

        super(Topic, self).save(*args, **kwargs)

        topic_processing.update_text_file(self)

        topic_processing.bind_linked_objects(self, document_model=Document, topic_model=Topic)

        self.last_saved = timezone.now()

        super(Topic, self).save(*args, **kwargs)

    def __unicode__(self):

        return self.key

    @property
    def title(self):

        return os.path.basename(self.key)

    @property
    def html(self):

        return topic_processing.text_to_html(self.text)

    def get_absolute_url(self):

        return reverse('hypothesize_app:topic_detail', kwargs={'key': self.key})