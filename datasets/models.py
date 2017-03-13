from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from os import path

file_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)

class Dataset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')

    # For database
    #data = models.TextField()
    # For media
    data = models.FileField(storage=file_storage)
    
    #Rating
    #Owner
    owner = models.ForeignKey('auth.User', related_name='datasets', on_delete=models.CASCADE)

    def filename(self):
        return path.basename(self.data.name) 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)


