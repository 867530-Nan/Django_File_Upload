from django.db import models

# Create your models here.


class Upload(models.Model):
    title = models.CharField(max_length=100)
    upload = models.FileField(upload_to="media/")

    def __str__(self):
        return self.title
