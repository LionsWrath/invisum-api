from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.db.models.functions import Coalesce
from datasets.choices import EXTENSION_CHOICES, STAR_CONVERSION
from os import path
import pandas as pd
import json

personal_location = path.join(settings.MEDIA_ROOT, 'personal')
personal_url = path.join(settings.MEDIA_URL, 'personal')

file_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
personal_storage = FileSystemStorage(location=personal_location, base_url=personal_url)

def update_filename(instance, filename):
    date = instance.created_at.strftime('%Y-%m-%d_%H-%M-%S')
    return '{0}_{1}.{2}'.format(instance.owner.username, 
                                date, 
                                instance.get_extension_display().lower()) 

# Encoding of the files may be a future problem
# Need reconfigurable fields for each type of file
class Dataset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    about = models.TextField(blank=True)

    data = models.FileField(storage=file_storage, upload_to=update_filename)    
    extension = models.IntegerField(choices=EXTENSION_CHOICES, default='CSV')

    @property
    def rating(self): 
        return Rating.objects.filter(dataset__id=self.id).aggregate(average=Coalesce(Avg('value'),0))
    
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
        ordering = ('created_at',)

class PersonalDataset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.TextField()

    original = models.ForeignKey(Dataset, related_name='personal', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='personal', on_delete=models.CASCADE)

    personal_data = models.FileField(storage=personal_storage, editable=False)    

    class Meta:
        ordering = ('created_at',)
 

class Rating(models.Model):
    owner = models.ForeignKey('auth.User', related_name='ratings', on_delete=models.CASCADE) 
    dataset = models.ForeignKey(Dataset, related_name='ratings', on_delete=models.CASCADE)

    value = models.PositiveSmallIntegerField(choices=STAR_CONVERSION)

    class Meta:
        ordering = ('dataset',)
        unique_together = (('owner', 'dataset'),)
