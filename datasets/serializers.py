from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from django.contrib.auth.models import User
from datasets.models import Dataset, Rating

class DatasetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dataset
        fields = ('id', 'title', 'data', 'extension', 'rating', 'owner')

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=serializers.CurrentUserDefault())

    # Dont know if setting None is a good practice in this case
    dataset = serializers.PrimaryKeyRelatedField(
            read_only=True,
            allow_null=True,
            default=serializers.CreateOnlyDefault(None))

    class Meta:
        model = Rating
        fields = ('id', 'owner', 'dataset', 'value')
        validators = [
            UniqueTogetherValidator(
                queryset=Rating.objects.all(),
                fields=('owner', 'dataset')
            )
        ]

class UserSerializer(serializers.ModelSerializer):
    datasets = serializers.PrimaryKeyRelatedField(many=True, queryset=Dataset.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'datasets')
