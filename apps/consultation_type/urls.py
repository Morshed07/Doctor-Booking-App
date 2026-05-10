from django.urls import path
from .views import ConsultationTypeListView


urlpatterns = [
    path(
        'types/',
        ConsultationTypeListView.as_view(),
        name='consultation-types'
    ),
]