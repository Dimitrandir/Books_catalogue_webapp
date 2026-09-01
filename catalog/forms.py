from django import forms

from .models import Book, Copy


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'genres', 'publisher', 'year', 'summary', 'cover_image']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }


class CopyForm(forms.ModelForm):
    class Meta:
        model = Copy
        fields = ['location', 'condition']
