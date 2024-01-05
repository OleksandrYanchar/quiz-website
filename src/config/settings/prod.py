import os

from dotenv import load_dotenv

from .base import *

ALLOWED_HOSTS = []

load_dotenv()

DEBUG = bool(os.environ.get("DEBUG"))