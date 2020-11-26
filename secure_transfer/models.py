from datetime import timedelta
from secrets import token_urlsafe

from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    user_agent = models.CharField(max_length=100)


class ProtectedItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name="items_created", on_delete=models.CASCADE
    )
    token = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    accessed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.token} by {self.owner} created at {self.created} accessed {self.accessed} times"

    @property
    def is_expired(self):
        return self.created + timedelta(hours=24) < timezone.now()

    def count_correct_redirect(self):
        self.accessed += 1

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.token = token_urlsafe()
        super(ProtectedItem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("protected", args=[self.token])


class ProtectedFile(ProtectedItem):
    uploaded_file = models.FileField()


class ProtectedUrl(ProtectedItem):
    url = models.URLField(max_length=2048)
