from rest_framework import generics
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListAPIView(generics.ListAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        # Start with the base queryset
        queryset = Doctor.objects.filter(is_available=True).prefetch_related('services')
        
        # Get the service ID from query parameters
        service_id = self.request.query_params.get('service_id')
        
        if service_id:
            # Filter doctors who have this specific service in their 'services' M2M field
            queryset = queryset.filter(services__id=service_id)
            
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'message': 'Doctors fetched successfully',
            'data': response.data,
        })
