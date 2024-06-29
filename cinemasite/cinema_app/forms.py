from django import forms
from .models import Cinema


class AddFilmsForm(forms.ModelForm):

    class Meta:
        model = Cinema
        fields = ['title', 'descriptions', 'year_production', 'is_active', 'cat', 'genres', 'photo']
