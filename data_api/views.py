from rest_framework import generics, permissions, status, exceptions
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer, OAuthTokenSerializer
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

class ItemListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating items.
    
    GET: List items for the authenticated user with optional filtering:
    - title: Case-insensitive partial match
    - created_after: Filter items created after this date (YYYY-MM-DD)
    - created_before: Filter items created before this date (YYYY-MM-DD)
    - order_by: Order results by field (title, created_at)
    
    POST: Create a new item associated with the authenticated user.
    
    Security:
    - Requires authentication
    - Only shows items owned by the authenticated user
    """
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return filtered queryset based on query parameters.
        
        Raises:
            PermissionDenied: If user attempts to access items they don't own
        """
        try:
            user = self.request.user
            queryset = Item.objects.filter(owner=user)
            
            # Apply filters
            title = self.request.query_params.get('title', None)
            if title:
                queryset = queryset.filter(title__icontains=title)
                
            created_after = self.request.query_params.get('created_after', None)
            if created_after:
                queryset = queryset.filter(created_at__gte=created_after)
                
            created_before = self.request.query_params.get('created_before', None)
            if created_before:
                queryset = queryset.filter(created_at__lte=created_before)
                
            order_by = self.request.query_params.get('order_by', 'created_at')
            if order_by in ['title', 'created_at']:
                queryset = queryset.order_by(order_by)
                
            return queryset
            
        except Exception as e:
            logger.error(f"Error in get_queryset: {str(e)}")
            raise exceptions.APIException("Failed to retrieve items")

    def perform_create(self, serializer):
        """
        Save the item instance and associate it with the logged-in user.
        
        Raises:
            PermissionDenied: If user is not authenticated
        """
        try:
            serializer.save(owner=self.request.user)
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}")
            raise exceptions.APIException("Failed to create item")

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific item.
    
    GET: Retrieve item details
    PUT/PATCH: Update item
    DELETE: Delete item
    
    Security:
    - Requires authentication
    - Only allows access to items owned by the authenticated user
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users can only access their own items.
        
        Raises:
            PermissionDenied: If user attempts to access items they don't own
        """
        user = self.request.user
        return Item.objects.filter(owner=user)

    def perform_destroy(self, instance):
        """
        Delete the item instance.
        
        Raises:
            PermissionDenied: If user is not the owner of the item
        """
        if instance.owner != self.request.user:
            raise PermissionDenied("You cannot delete items that don't belong to you")
        instance.delete()

class OAuthTokenView(generics.RetrieveAPIView):
    """
    API view for retrieving OAuth token information.
    
    GET: Retrieve user's OAuth token information
    
    Security:
    - Requires authentication
    - Only returns token information for the authenticated user
    """
    serializer_class = OAuthTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve the OAuth token for the authenticated user.
        
        Raises:
            PermissionDenied: If user is not authenticated
            exceptions.NotFound: If token does not exist
        """
        try:
            return self.request.user.google_token
        except Exception as e:
            logger.error(f"Error in get_object: {str(e)}")
            raise exceptions.NotFound("OAuth token not found")

class ProtectedItemListView(generics.ListAPIView):
    """
    API view for listing items with additional security measures.
    
    GET: List items with authentication required
    
    Security:
    - Requires authentication
    - Uses lookup_field for secure item identification
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated] 
    lookup_field = 'pk'
    
    def get_queryset(self):
        """
        Return items owned by the authenticated user.
        
        Raises:
            PermissionDenied: If user attempts to access items they don't own
        """
        return Item.objects.filter(owner=self.request.user)
