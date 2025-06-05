import os
import uuid
import magic
from supabase import create_client
from dotenv import load_dotenv
from django.conf import settings

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_PROJECT_URL")
supabase_key = os.environ.get("SUPABASE_ANON_KEY")
bucket_name = "daurtani"

supabase = create_client(supabase_url, supabase_key)

def get_file_mime_type(file):
    """Get the MIME type of a file."""
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read(1024))
    file.seek(0)  # Reset file pointer
    return file_type

def upload_image_to_supabase(file, folder="products"):
    """
    Upload an image to Supabase storage.
    
    Args:
        file: The file object to upload
        folder: The folder to upload to (default: "products")
        
    Returns:
        tuple: (image_path, image_url) if successful, (None, None) otherwise
    """
    try:
        # Generate a unique filename to prevent overwriting
        file_extension = os.path.splitext(file.name)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"{folder}/{unique_filename}"
        
        # Get file mime type
        mime_type = get_file_mime_type(file)
        
        # Upload file to Supabase
        supabase.storage.from_(bucket_name).upload(
            file_path,
            file.read(),
            {"content-type": mime_type}
        )
        
        # Get public URL
        file_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        
        return file_path, file_url
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        return None, None

def delete_image_from_supabase(file_path):
    """
    Delete an image from Supabase storage.
    
    Args:
        file_path: The path of the file to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase.storage.from_(bucket_name).remove([file_path])
        return True
    except Exception as e:
        print(f"Error deleting from Supabase: {e}")
        return False 