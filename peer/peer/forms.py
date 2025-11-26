from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Listing, Message, Profile


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "location", "is_request", "price"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["sender_name", "content"]


class UserRegistrationForm(UserCreationForm):
    skills = forms.CharField(max_length=300, required=False)
    town = forms.CharField(max_length=100, required=False)
    zipcode = forms.CharField(max_length=20, required=False)
    state = forms.CharField(max_length=50, required=False)

    class Meta:
        model = get_user_model()
        fields = ("username",)

    def save(self, commit=True):
        user = super().save(commit=commit)
        # create profile with provided data
        Profile.objects.create(
            user=user,
            skills=self.cleaned_data.get("skills", ""),
            town=self.cleaned_data.get("town", ""),
            zipcode=self.cleaned_data.get("zipcode", ""),
            state=self.cleaned_data.get("state", ""),
        )
        return user
