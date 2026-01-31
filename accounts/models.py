from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    # Add custom fields here if needed in future (e.g. phone, bio)
    pass


