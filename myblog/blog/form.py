# blog/forms.py
from django import forms

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
