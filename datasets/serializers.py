from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from django.contrib.auth.models import User
from datasets.models import Dataset, Rating, PersonalDataset

# Maybe change the value used to serialize

class DatasetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dataset
        fields = ('id', 'created_at', 'title', 'about', 'data', 'extension', 'rating', 'owner')

class PersonalDatasetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    original = serializers.ReadOnlyField(source='original.id')

    class Meta:
        model = PersonalDataset
        fields = ('id', 'created_at', 'updated_at', 'description', 'original', 'owner', 'personal_data')

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    dataset = serializers.ReadOnlyField(source='dataset.id')

    # Add a error message here after
    class Meta:
        model = Rating
        fields = ('id', 'owner', 'dataset', 'value')

class UserSerializer(serializers.ModelSerializer):
    datasets = serializers.PrimaryKeyRelatedField(many=True, queryset=Dataset.objects.all())

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'datasets')
