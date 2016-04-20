from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from hypothesize_app.models import Document, Supplement, Node, NodeType


class DocumentForm(ModelForm):
    """Document form."""
    class Meta:
        model = Document
        fields = ['title', 'author_text', 'publication', 'year', 'abstract', 'file', 'web_link', 'linked_document_text']


class SupplementForm(ModelForm):
    """Supplementary material form."""
    class Meta:
        model = Supplement
        fields = ['file']


class NodeForm(ModelForm):
    """
    Form for changing a node's contents.
    """
    class Meta:
        model = Node
        fields = ['id', 'type', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 60, 'cols': 120})
        }


class NodeTypeForm(ModelForm):
    """
    Form for changing a node type's contents.
    """
    class Meta:
        model = NodeType
        fields = ['id', 'description', 'text_template']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 120})
        }


class DocumentSearchForm(forms.Form):
    """
    Form for searching documents database.
    """
    query = forms.CharField(label='document_query', max_length=500)


class NodeSearchForm(forms.Form):
    """
    Form for searching node database.
    """
    query = forms.CharField(label='node_query', max_length=500)