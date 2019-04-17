from django import forms
from autos.models import Auto

# NOTE: Help from Danny Teng

# Create the form class.
class CreateForm(forms.ModelForm):

    class Meta:
        model = Auto
        fields = ['name', 'detail', 'mileage']

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
