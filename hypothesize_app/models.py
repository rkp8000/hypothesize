from __future__ import print_function, unicode_literals
import os

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

import document_processing
import node_processing


class Author(models.Model):
    """Author class."""

    id = models.CharField(max_length=255, primary_key=True)

    def __unicode__(self):

        return self.id


class Document(models.Model):
    """Article class."""

    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255, default='')
    author_text = models.TextField(blank=True, default='')
    publication = models.CharField(max_length=100, blank=True, default='')
    year = models.SmallIntegerField(null=True, blank=True)
    abstract = models.TextField(blank=True, default='')
    web_link = models.CharField(max_length=500, blank=True, default='')
    last_viewed = models.DateTimeField(default=timezone.now, blank=True)
    uploaded = models.DateTimeField(default=timezone.now, blank=True)
    file = models.FileField(upload_to='documents', null=True, blank=True)
    linked_document_text = models.TextField(blank=True, default='')
    linked_documents = models.ManyToManyField('self', symmetrical=False, blank=True)
    authors = models.ManyToManyField(Author, blank=True)

    def __unicode__(self):

        return self.id

    @property
    def primary_external_link(self):

        if self.web_link:

            return self.web_link

        else:

            return document_processing.google_scholar_search_url(self)

    def get_absolute_url(self):

        return reverse('hypothesize_app:document_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """
        Override basic save method to extract linked documents.
        """

        # generate id if there wasn't one before

        if not self.id:

            document_processing.bind_primary_key(self, document_model=Document)

        else:

            # change document id if primary key base has changed

            pk_base = document_processing.get_primary_key_base(self.id)

            if pk_base != document_processing.make_candidate_primary_key(self):

                document_processing.bind_primary_key(self, document_model=Document)

        # save the document so we can bind other things to it

        super(Document, self).save(*args, **kwargs)

        document_processing.bind_authors(self, author_model=Author)

        document_processing.bind_linked_documents(self, document_model=Document)

        super(Document, self).save(*args, **kwargs)


class Node(models.Model):
    """Node class."""

    id = models.CharField(max_length=1000, primary_key=True)
    text = models.TextField(blank=True, default='')
    last_viewed = models.DateTimeField(default=timezone.now, blank=True)
    nodes = models.ManyToManyField('self', symmetrical=False, blank=True)
    documents = models.ManyToManyField(Document, blank=True)

    def save(self, *args, **kwargs):
        """
        Override default method to do additional node processing.
        """

        # save the node so we can bind other things to it

        super(Node, self).save(*args, **kwargs)

        node_processing.update_text_file(self)

        node_processing.bind_linked_objects(self, document_model=Document, node_model=Node)

        super(Node, self).save(*args, **kwargs)

    def __unicode__(self):

        return self.id

    @property
    def title(self):

        return os.path.basename(self.id)

    @property
    def html(self):

        return node_processing.text_to_html(self.text)

    def get_absolute_url(self):

        return reverse('hypothesize_app:node_detail', kwargs={'pk': self.id})