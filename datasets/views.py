from datasets.models import Dataset, PersonalDataset, Rating
from datasets.serializers import DatasetSerializer
from datasets.serializers import UserSerializer
from datasets.serializers import RatingSerializer
from datasets.serializers import PersonalDatasetSerializer
from datasets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import generics
from rest_framework import permissions
from os import path
import uuid

# Sent the 10 best ranked datasets
class DiscoverFeed(generics.ListAPIView):
    serializer_class = DatasetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        dataframes = sorted(Dataset.objects.all(), key=lambda t: t.rating)
        return dataframes[:10] 

# Search a Dataset by title (case insensitive)
class DatasetByName(generics.ListAPIView):
    serializer_class = DatasetSerializer

    def get_queryset(self):
        title = self.kwargs['title']
        return Dataset.objects.filter(title__icontains=title)

# Search a Dataset by user (case insensitive)
class DatasetByUser(generics.ListAPIView):
    serializer_class = DatasetSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Dataset.objects.filter(owner__username__icontains=username)


# Downloadable files for logged users by filename
class DatasetServeByFilename(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, filename):
        response = Response(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
        response['X-Sendfile'] = smart_str(path.join(settings.MEDIA_ROOT, filename))
        
        return response

# Downloadable files for logged users by dataset id
class DatasetServeById(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        dataset = Dataset.objects.get(pk = pk)

        response = Response(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(dataset.filename())
        response['X-Sendfile'] = smart_str(dataset.data.url)
        
        return response

class DatasetList(generics.ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    # Associate a User to the Dataset - POST
    def perform_create(self, instance):
        instance.save(owner=self.request.user)

class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_destroy(self, instance):
        instance.data.delete(False)
        instance.delete()

# Testing
# List all personal datasets of a user
class PersonalDatasetList(generics.ListAPIView):
    serializer_class = PersonalDatasetSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    
    def get_queryset(self):
        return PersonalDataset.objects.filter(owner=self.request.user)

# Create a new personal dataset based on a original
# List based on a dataset
class PersonalDatasetCreate(generics.ListCreateAPIView):
    serializer_class = PersonalDatasetSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        dataset = self.kwargs['dataset']

        return PersonalDataset.objects.filter(original__id=dataset, owner=user)

    # Associate the user and the dataset to the rating
    # Validating the unique together constraint
    def perform_create(self, instance):
        user = self.request.user
        dataset = self.kwargs['dataset']

        try:
            dataset = Dataset.objects.get(pk=dataset)
        except ObjectDoesNotExist:
            raise NotFound(_('Wrong value for dataset query.'))

        new_file = ContentFile(dataset.data.read())
        new_file.name = '.'.join([str(uuid.uuid4()), dataset.get_extension_display().lower()])

        instance.save(owner=user, original=dataset, personal_data=new_file)

class PersonalDatasetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalDataset.objects.all()
    serializer_class = PersonalDatasetSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_destroy(self, instance):
        instance.personal_data.delete(False)
        instance.delete()
     

# Create a ViewSet for the user later
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List by Dataset/User
class RatingList(generics.ListCreateAPIView):
    serializer_class = RatingSerializer

    # Check this permissions - is read only permitted?
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
   
    def get_queryset(self):
        dataset = self.kwargs['dataset']
        return Rating.objects.filter(dataset__pk=dataset, owner=self.request.user)

    # Associate the user and the dataset to the rating
    # Validating the unique together constraint
    def perform_create(self, instance):
        user = self.request.user
        dataset = self.kwargs['dataset']

        if Rating.objects.filter(dataset=dataset, owner=user).exists():            
            raise ValidationError(_('The User already rated this dataset.'))

        try:
            dataset = Dataset.objects.get(pk=self.kwargs['dataset'])
        except ObjectDoesNotExist:
            raise NotFound(_('Wrong value for dataset query.'))

        instance.save(owner=user, dataset=dataset)

class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
