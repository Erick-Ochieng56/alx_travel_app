"""
Views for the listings app.
"""
from rest_framework import viewsets, permissions
from .models import Listing, ListingImage
from .serializers import ListingSerializer, ListingImageSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing listings
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """
        Optionally restricts the returned listings by filtering
        against query parameters in the URL.
        """
        queryset = Listing.objects.all()
        
        # Filter by listing type
        listing_type = self.request.query_params.get('type')
        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)
            
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
            
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
            
        # Filter by number of guests
        guests = self.request.query_params.get('guests')
        if guests:
            queryset = queryset.filter(max_guests__gte=guests)
            
        return queryset


class ListingImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing listing images
    """
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        serializer.save(listing_id=listing_id)