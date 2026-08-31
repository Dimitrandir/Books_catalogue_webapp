from django import forms

from .models import Loan


class LendForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['person', 'date_given']
        widgets = {
            'date_given': forms.DateInput(attrs={'type': 'date'}),
        }
