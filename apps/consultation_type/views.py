from django.shortcuts import render
from rest_framework import generics
from .models import ConsultationType
from .serializers import ConsultationTypeSerializer
from rest_framework.response import Response

# Create your views here.


class ConsultationTypeListView(generics.ListAPIView):
    serializer_class = ConsultationTypeSerializer
    queryset = ConsultationType.get_available_consultation_types()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'Consultation types fetched successfully',
            'data': response.data,
        })
