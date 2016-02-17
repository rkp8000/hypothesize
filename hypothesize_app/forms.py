from django import forms
from django.forms import ModelForm
from django.forms import modelformset_factory
from hypothesize_app.models import Document, Author, Supplement, Node, NodeType


class DocumentForm(ModelForm):
    """Document form."""
    class Meta:
        model = Document
        fields = ['title', 'publication', 'year', 'abstract', 'file', 'web_link']


class SupplementForm(ModelForm):
    """Supplementary material form."""
    class Meta:
        model = Supplement
        fields = ['file']


class AuthorForm(ModelForm):
    """Author form."""
    class Meta:
        model = Author
        fields = ['first_name', 'middle_names', 'last_name']


AuthorFormSet = modelformset_factory(Author, form=AuthorForm, extra=30)


class NodeForm(ModelForm):
    """
    Form for changing a node's contents.
    """
    class Meta:
        model = Node
        fields = ['id', 'type', 'title', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 60, 'cols': 120})
        }


class DocumentSearchForm(forms.Form):
    """
    Form for searching documents database.
    """
    query = forms.CharField(label='document_query', max_length=500)

    def get_articles_from_query(self):
        # search first author, titles, abstracts
        documents = []
        document_set_id = Document.objects.filter(id__contains=self.cleaned_data['query'])
        documents += [document for document in document_set_id if document not in documents]
        document_set_title = Document.objects.filter(title__contains=self.cleaned_data['query'])
        documents += [document for document in document_set_title if document not in documents]
        document_set_abstract = Document.objects.filter(abstract__contains=self.cleaned_data['query'])
        documents += [document for document in document_set_abstract if document not in documents]
        return documents


class NodeSearchForm(forms.Form):
    """
    Form for searching node database.
    """
    query = forms.CharField(label='node_query', max_length=500)

    def get_nodes_from_query(self):
        # search first author, titles, abstracts
        nodes = []
        node_set_title = Node.objects.filter(title__contains=self.cleaned_data['query'])
        nodes += [node for node in node_set_title if node not in nodes]
        node_set_text = Node.objects.filter(text__contains=self.cleaned_data['query'])
        nodes += [node for node in node_set_text if node not in nodes]
        return nodes