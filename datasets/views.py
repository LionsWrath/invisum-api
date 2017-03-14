from datasets.models import Dataset
from datasets.serializers import DatasetSerializer
from datasets.serializers import UserSerializer
from datasets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
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

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
