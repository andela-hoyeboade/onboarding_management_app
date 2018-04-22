from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import UserRole


class User(AbstractUser):
    ROLE_CHOICES = (
        (int(UserRole.NORMAL_USER), 'Normal User',),
        (int(UserRole.DEPARTMENT_ADMIN), 'Department Admin',),
        (int(UserRole.SUPER_USER), 'Super User',),)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=int(UserRole.NORMAL_USER))

    class Meta:
        unique_together = ('email',)

    def __str__(self):
        return '<User username={0}>'.format(self.username)
