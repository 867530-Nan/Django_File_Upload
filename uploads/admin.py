from django.contrib import admin

from .models import Upload, URLUpload, Word

admin.site.register(Upload)
admin.site.register(URLUpload)
admin.site.register(Word)
