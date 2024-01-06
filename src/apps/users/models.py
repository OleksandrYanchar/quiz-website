import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import BaseModel

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    slug = models.SlugField(max_length=256)
    date_added = models.DateTimeField(auto_now=True)
    date_changed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)