from django.contrib import admin

from .models import Author, Document, Supplement, NodeType, Node

admin.site.register(Author)
admin.site.register(Document)
admin.site.register(Supplement)
admin.site.register(NodeType)
admin.site.register(Node)