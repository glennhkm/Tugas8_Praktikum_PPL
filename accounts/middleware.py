import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import login

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users via JWT tokens stored in cookies.
    This is used to maintain authentication state across requests.
    """
    
    def process_request(self, request):
        # Skip authentication if user is already authenticated
        if request.user.is_authenticated:
            return None
        
        # Get the token from cookies
        token = request.COOKIES.get('access_token')
        if not token:
            return None
            
        try:
            # Validate the token
            UntypedToken(token)
            
            # Get the user ID from the token
            decoded_data = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
            user_id = decoded_data['user_id']
            
            # Get the user and login
            user = User.objects.get(id=user_id)
            login(request, user)
            
        except (InvalidToken, TokenError, jwt.PyJWTError, User.DoesNotExist):
            # If token is invalid or expired, remove it
            if hasattr(request, 'delete_cookie'):
                request.delete_cookie('access_token')
            
        return None 