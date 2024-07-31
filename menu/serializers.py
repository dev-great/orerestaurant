from rest_framework import serializers

from authorization.serializers import UserSerializer

from .models import MenuItem, MenuItemImage, MenuItemTag, Rating, Review


class MenuItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemImage
        fields = '__all__'


class MenuItemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemTag
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    tags = MenuItemTagSerializer(many=True, required=False)

    class Meta:
        model = MenuItem
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
