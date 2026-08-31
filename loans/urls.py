from django.urls import path

from . import views

app_name = 'loans'

urlpatterns = [
    path('copies/<int:copy_id>/lend/', views.lend_copy, name='lend_copy'),
    path('loans/<int:loan_id>/return/', views.return_loan, name='return_loan'),
]
