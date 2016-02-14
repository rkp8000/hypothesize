from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from unidecode import unidecode


class Document(models.Model):
    """Article class."""
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    journal = models.CharField(max_length=100, blank=True, default='')
    year = models.SmallIntegerField(null=False, blank=True, default=0)
    abstract = models.TextField(blank=True, default='')
    web_link = models.CharField(max_length=500, blank=True, default='')
    last_viewed = models.DateTimeField(default=datetime.now, blank=True)
    uploaded = models.DateTimeField(default=datetime.now, blank=True)
    file = models.FileField(upload_to='articles', null=True, blank=True)

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
    supplement_file = models.FileField(upload_to='supplementary', null=True)
    article = models.ForeignKey(Document)

    def __unicode__(self):
        return self.id