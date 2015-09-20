from django import forms
from django.core.exceptions import ValidationError

from munchee.models import Company


class CompanyForm(forms.Form):
    companies = forms.CharField(
        label = "e.g. Google, Apple, Bloomberg, ...",
        required = True,
    )
    keywords = forms.CharField(
        label = "e.g. software, technology, ...",
        required = False,
    )

class OAuthCallbackForm(forms.Form):
    code = forms.CharField()
    state = forms.CharField()