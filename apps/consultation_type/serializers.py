from rest_framework import serializers
from .models import ConsultationType


class ConsultationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationType
        fields = [
            'id',
            'name',
            'description',
            'fee',
            'is_available',
            'is_recommended',
            'facility_1',
            'facility_2',
            'facility_3',
            'facility_4',
            'facility_5',
            'facility_6',
        ]
