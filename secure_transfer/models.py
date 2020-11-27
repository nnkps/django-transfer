from datetime import timedelta
from mimetypes import guess_type
from secrets import token_urlsafe

from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string


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

    def create_random_password(self):
        password = get_random_string()
        self.set_password(password)
        return password

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

    def get_response(self):
        if hasattr(self, "protectedurl"):
            return redirect(self.protectedurl.url)

        file_ = self.protectedfile.uploaded_file
        filename = str(file_)[1:]
        content_type = guess_type(filename)[0]
        response = HttpResponse(
            file_.read(),
            content_type=content_type,
        )
        disposition = "inline" if content_type.startswith("image") else "attachment"
        response["Content-Disposition"] = f'{disposition}; filename="{filename}"'
        return response


class ProtectedFile(ProtectedItem):
    uploaded_file = models.FileField()


class ProtectedUrl(ProtectedItem):
    url = models.URLField(max_length=2048)
