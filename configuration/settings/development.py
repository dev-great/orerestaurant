import os
from .base import *
import cloudinary
import cloudinary_storage
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv


load_dotenv()
environment = os.environ.get('ENVIRONMENT')

DEBUG = True

ALLOWED_HOSTS = ['orerestaurant.pythonanywhere.com',
                 '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CLOUDINARY_URL = 'cloudinary://387625877385614:zZrsexxvBVryHpiyJ6DG2tZrl5Y@dbrvleydy'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET'),
}

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
)


# Media files
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
