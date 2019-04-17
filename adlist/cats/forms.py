from django import forms
from cats.models import Cat

# NOTE: Help from Danny Teng

# Create the form class.
class CreateForm(forms.ModelForm):

    class Meta:
        model = Cat
        fields = ['name', 'foods', 'weight']

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
