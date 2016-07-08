from django.contrib import admin

import models

admin.site.register(models.Author)
admin.site.register(models.Document)
admin.site.register(models.Supplement)
admin.site.register(models.NodeType)
admin.site.register(models.Node)