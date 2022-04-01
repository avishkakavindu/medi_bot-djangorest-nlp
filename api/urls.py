from django.urls import path
from api import api_view

urlpatterns = [
    path('medibot/', api_view.MediBotAPIView.as_view(), name='medibot'),
    path('heart-disease-model/', api_view.HeartDiseaseAPIView.as_view(), name='heart_disease_model'),
]
