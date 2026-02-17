from django import forms
from passports.models import CompetencePassport


class CompetencePassportForm(forms.ModelForm):
    class Meta:
        model = CompetencePassport
        fields = ["headline", "summary", "verification_tier"]
