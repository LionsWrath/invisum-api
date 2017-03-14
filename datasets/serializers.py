from rest_framework import serializers
from django.contrib.auth.models import User
from datasets.models import Dataset, Rating

class DatasetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dataset
        fields = ('id', 'title', 'data', 'extension', 'rating', 'owner')

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    dataset = serializers.ReadOnlyField(source='dataset.id')

    class Meta:
        model = Rating
        fields = ('id', 'owner', 'dataset', 'value')


class UserSerializer(serializers.ModelSerializer):
    datasets = serializers.PrimaryKeyRelatedField(many=True, queryset=Dataset.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'datasets')
