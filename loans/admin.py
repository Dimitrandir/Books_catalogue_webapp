from django.contrib import admin

from .models import Loan, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['copy', 'person', 'date_given', 'date_returned']
    list_filter = ['person', 'date_returned']
    search_fields = ['copy__book__title', 'person__name']
    autocomplete_fields = ['copy', 'person']
