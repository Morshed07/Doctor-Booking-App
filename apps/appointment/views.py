from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment, AppointmentStatusHistory
from .serializers import AppointmentSerializer, AppointmentStatusHistorySerializer
from rest_framework.permissions import IsAuthenticated


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Appointment.objects.all()
        appointment_id = self.request.query_params.get('id')
        if appointment_id:
            queryset = queryset.filter(id=appointment_id)
        return queryset

    @action(detail=False, methods=['get'], url_path='booked-slots/(?P<doctor_id>[^/.]+)')
    def booked_slots(self, request, doctor_id=None):
        # Optional: Get start and end dates from query params
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        
        queryset = Appointment.objects.filter(doctor_id=doctor_id)
    
        if start_date and end_date:
            queryset = queryset.filter(appointment_time__range=[start_date, end_date])
            
        booked_times = queryset.values_list('appointment_time', flat=True).distinct()
        
        return Response({
            "booked_slots": [dt.isoformat() for dt in booked_times]
        })
        
    @action(detail=True, methods=['get'], permission_classes=[], url_path='payment-info')
    def payment_info(self, request, pk=None):
        appointment = Appointment.objects.get(id=pk)
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class AppointmentStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = AppointmentStatusHistory.objects.all()
    serializer_class = AppointmentStatusHistorySerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optional: Filter appointments by the email/phone if provided in query params
        queryset = AppointmentStatusHistory.objects.all()
        return queryset