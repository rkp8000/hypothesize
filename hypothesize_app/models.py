from __future__ import print_function, unicode_literals
from datetime import datetime
from unidecode import unidecode

from django.db import models

import node_processing


class Setting(models.Model):
    """Setting class."""
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=10, null=False)
    bool_value = models.BinaryField(null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)
    float_value = models.FloatField(null=True, blank=True)
    str_value = models.CharField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Override default save method so that we can do some extra stuff.
        """
        # do anything we need to do with the updated setting
        if self.id == 'NODE_SAVE_DIRECTORY':
            node_processing.make_node_save_directory(self.str_value)

        super(Setting, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @property
    def value(self):
        value_dict = {
            'bool': self.bool_value,
            'int': self.int_value,
            'float': self.float_value,
            'str': self.str_value,
        }
        return value_dict[self.type]


class Document(models.Model):
    """Article class."""
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    publication = models.CharField(max_length=100, blank=True, default='')
    year = models.SmallIntegerField(null=False, blank=True, default=0)
    abstract = models.TextField(blank=True, default='')
    web_link = models.CharField(max_length=500, blank=True, default='')
    last_viewed = models.DateTimeField(default=datetime.now, blank=True)
    uploaded = models.DateTimeField(default=datetime.now, blank=True)
    file = models.FileField(upload_to='documents', null=True, blank=True)
    linked_document_text = models.TextField(blank=True, default='')
    linked_documents = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __unicode__(self):
        return self.id

    @property
    def primary_external_link(self):
        if self.external_file_path:
            return self.external_file_path
        elif self.web_link:
            return self.web_link
        else:
            # TODO: make this return a google search for the article's title
            return None

    @property
    def id_clean(self):
        return unidecode(self.id)

    @property
    def title_clean(self):
        return unidecode(self.title)

    @property
    def abstract_clean(self):
        return unidecode(self.abstract)


class Author(models.Model):
    """Author class."""
    last_name = models.CharField(max_length=100, blank=True, default='')
    first_name = models.CharField(max_length=100, blank=True, default='')
    middle_names = models.CharField(max_length=100, blank=True, default='')
    document = models.ForeignKey(Document)


class Supplement(models.Model):
    """Supplementary materials class."""
    id = models.CharField(max_length=100, primary_key=True)
    file = models.FileField(upload_to='supplements', null=True)
    document = models.ForeignKey(Document)

    def __unicode__(self):
        return self.id


class NodeType(models.Model):
    """
    Node type class.
    """
    id = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True, default='')
    template_title = models.CharField(max_length=500, blank=True, default='')
    template = models.TextField(blank=True, default='')

    def __unicode__(self):
        return self.id


class Node(models.Model):
    """Node class."""
    id = models.CharField(max_length=1000, primary_key=True)
    type = models.ForeignKey(NodeType, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=500, null=False, default='untitled', blank=False, unique=True)
    text = models.TextField(blank=True, default='')
    last_viewed = models.DateTimeField(default=datetime.now, blank=True)
    nodes = models.ManyToManyField('self', symmetrical=False, blank=True)
    documents = models.ManyToManyField(Document, blank=True)

    def save(self, *args, **kwargs):
        """
        Override default method to do additional node processing.
        """

        node_processing.update_text_file(self, setting_model=Setting)
        node_processing.bind_linked_objects(self, document_model=Document, node_model=Node)

        super(Node, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.id

    @property
    def html(self):
        return node_processing.text_to_html(self.text)