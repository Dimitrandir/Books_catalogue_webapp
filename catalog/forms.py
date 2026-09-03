from django import forms
from django.urls import reverse_lazy

from .models import Book, Copy


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'genres', 'publisher', 'year', 'summary', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'hx-get': reverse_lazy('catalog:title_check'),
                'hx-trigger': 'keyup changed delay:400ms',
                'hx-target': '#title-check-result',
                'hx-swap': 'innerHTML',
                'hx-include': 'this, [name=exclude]',
            }),
            'summary': forms.Textarea(attrs={'rows': 4}),
        }


class CopyForm(forms.ModelForm):
    class Meta:
        model = Copy
        fields = ['location', 'condition']
