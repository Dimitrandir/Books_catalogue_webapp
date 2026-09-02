from django.urls import path

from . import views

app_name = 'scanner'

urlpatterns = [
    path('scan/', views.scan_cover, name='scan_cover'),
]
