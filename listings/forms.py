from django import forms
from .models import *


class ListingsImageForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title','description','picture','category','sub_category','unit']