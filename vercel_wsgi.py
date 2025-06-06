"""
Simplified WSGI file for Vercel deployment
"""

import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure PyMySQL
import pymysql
pymysql.install_as_MySQLdb()

# Handle pkg_resources issue with djangorestframework-simplejwt
try:
    # First try to import pkg_resources
    import pkg_resources
except ImportError:
    # If pkg_resources is not available, create a simple mock
    import types
    pkg_resources = types.ModuleType("pkg_resources")
    pkg_resources.DistributionNotFound = type("DistributionNotFound", (Exception,), {})
    def get_distribution(dist):
        return types.SimpleNamespace(version="0.0.0")
    pkg_resources.get_distribution = get_distribution
    sys.modules["pkg_resources"] = pkg_resources

    # Also patch the rest_framework_simplejwt module directly
    try:
        # Create a directory for the patched module
        os.makedirs("rest_framework_simplejwt", exist_ok=True)
        
        # Create a simple __init__.py file
        with open("rest_framework_simplejwt/__init__.py", "w") as f:
            f.write('__version__ = "5.3.0"\n')
        
        # Add the current directory to the path
        sys.path.insert(0, os.getcwd())
    except Exception as e:
        print(f"Failed to create patched module: {e}")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronic_store.settings')

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel handler
app = application 