from django.contrib import admin

from .models import Author, Document

admin.site.register(Author)
admin.site.register(Document)