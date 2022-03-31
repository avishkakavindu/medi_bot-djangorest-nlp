from django.urls import path
from api import api_view

urlpatterns = [
    path('medibot/', api_view.MediBotAPIView.as_view(), name='medibot'),
]