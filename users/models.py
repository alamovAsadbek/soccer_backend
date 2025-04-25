from django.contrib.auth.models import AbstractUser
from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    isAdmin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)

    # Groups maydoniga related_name qo'shish
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # related_name ni o'zgartirdik
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )

    # User Permissions maydoniga related_name qo'shish
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # related_name ni o'zgartirdik
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.username
