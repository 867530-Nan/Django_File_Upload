from django.contrib import admin

from .models import Upload, URLUpload

admin.site.register(Upload)
admin.site.register(URLUpload)
