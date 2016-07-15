from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from hypothesize_app.models import Document, Topic

MAX_HIT_OPTIONS = [(20, 20), (50, 50), (100, 100)]


class DocumentForm(ModelForm):
    """Document form."""

    class Meta:

        model = Document
        fields = [
            'title', 'author_text', 'publication', 'year',
            'abstract', 'file', 'web_link', 'linked_document_text',
            'crossref'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'web_link': forms.TextInput(attrs={'size': 80}),
            'publication': forms.TextInput(attrs={'size': 40}),
            'author_text': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'abstract': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
            'crossref': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'linked_document_text': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
        }


class TopicForm(ModelForm):
    """
    Form for changing a topic's contents.
    """

    class Meta:

        model = Topic
        fields = ['key', 'text']
        labels = {
            'key': 'key',
            'text': mark_safe(
                'Text'
                '&nbsp; &nbsp; <span id="topic_save_status"></span><br />'),
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 60, 'cols': 120})
        }


class DocumentSearchForm(forms.Form):
    """
    Form for searching documents database.
    """

    query = forms.CharField(label='document_query', max_length=500)
    max_hits = forms.ChoiceField(label='max_hits', choices=MAX_HIT_OPTIONS)


class TopicSearchForm(forms.Form):
    """
    Form for searching topic database.
    """

    query = forms.CharField(label='topic_query', max_length=500)
    max_hits = forms.ChoiceField(label='max_hits', choices=MAX_HIT_OPTIONS)