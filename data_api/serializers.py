from rest_framework import serializers
from .models import Item, GoogleOAuthToken

class OAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleOAuthToken
        fields = ['access_token', 'refresh_token', 'token_expires_at']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'owner']
        read_only_fields = ['owner'] # owner will be set automatically based on the logged-in user