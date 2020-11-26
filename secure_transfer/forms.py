from django import forms
from django.core.exceptions import ValidationError

from .models import ProtectedItem


class ProtectedWithPasswordForm(forms.Form):
    token = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get("token")
        password = cleaned_data.get("password")

        if token and password:
            self.item = ProtectedItem.objects.get(token=token)
            if not self.item or not self.item.check_password(password):
                raise ValidationError("wrong password")

            if self.item.is_expired:
                raise ValidationError("link expired")
