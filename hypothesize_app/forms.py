from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from hypothesize_app.models import Document, Thread

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


class ThreadForm(ModelForm):
    """
    Form for changing a thread's contents.
    """

    class Meta:

        model = Thread
        fields = ['key', 'text']
        widgets = {
            'key': forms.TextInput(attrs={'size': 80}),
        }


class DocumentSearchForm(forms.Form):
    """
    Form for searching documents database.
    """

    query = forms.CharField(
        label='document_query', max_length=500, widget=forms.TextInput(attrs={'size': 50}))
    max_hits = forms.ChoiceField(label='max_hits', choices=MAX_HIT_OPTIONS)


class ThreadSearchForm(forms.Form):
    """
    Form for searching thread database.
    """

    query = forms.CharField(
        label='thread_query', max_length=500, widget=forms.TextInput(attrs={'size': 50}))
    max_hits = forms.ChoiceField(label='max_hits', choices=MAX_HIT_OPTIONS)