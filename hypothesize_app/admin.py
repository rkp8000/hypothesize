from django.contrib import admin

from .models import Author, Document, Supplement

admin.site.register(Author)
admin.site.register(Document)
admin.site.register(Supplement)