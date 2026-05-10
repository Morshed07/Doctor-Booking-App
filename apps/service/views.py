from django.shortcuts import render
from .models import Service
from .serializers import ServiceSerializer
from rest_framework import generics
from rest_framework.response import Response


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'Services fetched successfully',
            'data': response.data,
        })
