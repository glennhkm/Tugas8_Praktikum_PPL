"""
Simplified version of djangorestframework-simplejwt authentication
"""

from rest_framework.authentication import BaseAuthentication

class JWTAuthentication(BaseAuthentication):
    """
    Simplified JWT authentication class
    """
    def authenticate(self, request):
        return None
