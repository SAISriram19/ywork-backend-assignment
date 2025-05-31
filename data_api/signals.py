from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import GoogleOAuthToken
from allauth.socialaccount.models import SocialToken

User = get_user_model()

@receiver(post_save, sender=SocialToken)
def store_google_tokens(sender, instance, created, **kwargs):
    if instance.provider == 'google':
        user = instance.account.user
        
        # Update or create the token record
        GoogleOAuthToken.objects.update_or_create(
            user=user,
            defaults={
                'access_token': instance.token,
                'refresh_token': instance.refresh_token if instance.refresh_token else '',
                'token_expires_at': instance.expires_at
            }
        )
