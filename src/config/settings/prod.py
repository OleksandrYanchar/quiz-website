import os

from dotenv import load_dotenv

from .base import *

DEBUG = False
ALLOWED_HOSTS = []  # Add hosts before deploy

load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
