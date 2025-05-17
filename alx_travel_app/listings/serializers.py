"""
Serializers for the listings app.
"""
from rest_framework import serializers
from .models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    """
    Serializer for listing images
    """
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'is_primary', 'caption', 'upload_date']


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for listings
    """
    images = ListingImageSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'listing_type', 'price_per_night',
                 'location', 'address', 'max_guests', 'bedrooms', 'bathrooms',
                 'amenities', 'owner', 'owner_name', 'is_active', 'created_at',
                 'updated_at', 'images']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner.get_full_name() else obj.owner.username