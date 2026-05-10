from django.urls import path
from .views import DoctorListAPIView


urlpatterns = [
    path('doctors/', DoctorListAPIView.as_view(), name='doctors'),
]
