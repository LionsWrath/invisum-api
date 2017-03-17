from datasets.models import Dataset, Rating
from datasets.serializers import DatasetSerializer
from datasets.serializers import UserSerializer
from datasets.serializers import RatingSerializer
from datasets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework import permissions
from os import path

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

    # Associate a User to the Dataset
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
   
    def get_queryset(self):
        dataset = self.kwargs['dataset']
        return Rating.objects.filter(dataset__pk=dataset, owner=self.request.user)

    # Associate the user and the dataset to the rating
    # Validating the unique together constraint
    def perform_create(self, serializer):
        user = self.request.user
        dataset = self.kwargs['dataset']

        if Rating.objects.filter(dataset=dataset, owner=user).exists():            
            raise ValidationError(_('The User already rated this dataset.'))

        dataset = Dataset.objects.get(pk=self.kwargs['dataset'])
        
        serializer.save(owner=user, dataset=dataset)

class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
