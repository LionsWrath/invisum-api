from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from datasets.choices import EXTENSION_CHOICES
from os import path
import pandas as pd
import json

file_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)

def update_filename(instance, filename):
    date = instance.created.strftime('%Y-%m-%d_%H-%M-%S')
    return '{0}_{1}.{2}'.format(instance.owner.username, 
                                date, 
                                instance.get_extension_display().lower()) 

class Dataset(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')

    # For media
    data = models.FileField(storage=file_storage, upload_to=update_filename)    
    extension = models.CharField(choices=EXTENSION_CHOICES, default='CSV', max_length=20)
    
    #Encoding may be a problem

    #Rating
    #Owner
    owner = models.ForeignKey('auth.User', related_name='datasets', on_delete=models.CASCADE)
    
    def process_json(self, url):
        records = [json.loads(line) for line in open(url)]
        return pd.DataFrame(records)

    def process_csv(self, url):
        return pd.read_csv(url)

    def process_excel(self, url):
        return pd.read_excel(url)

    def process_table(self, url):
        return pd.read_table()

    def to_dataframe(self):
        method = {
            '1' : self.process_csv,
            '2' : self.process_json,
            '3' : self.process_excel,
            '4' : self.process_table,
        }[self.extension]

        url = path.join(settings.MEDIA_ROOT, self.filename())

        return method(url)

    def filename(self):
        return path.basename(self.data.name) 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)


